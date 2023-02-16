import os
import json
import requests
from netrc import netrc
from subprocess import Popen
from platform import system
from getpass import getpass
import warnings
import logging
import  sys
from functools import partial
from boto3 import Session
from botocore.session import get_session
from botocore.credentials import RefreshableCredentials, DeferredRefreshableCredentials
from aiobotocore.session import get_session as aio_get_session
from aiobotocore.credentials import AioRefreshableCredentials
from botocore.client import Config

warnings.filterwarnings('ignore')
logging.basicConfig(format='%(levelname)s : %(message)s', level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
# Earthdata URL endpoint for authentication
urs = "urs.earthdata.nasa.gov"
# this will make the total refresh time before 15 mins of expiration of credentials
ADVISORY_REFRESH_TIMEOUT = 59 * 60  # 15 min
MANDATORY_REFRESH_TIMEOUT = 58 * 60  # 10 min


def _validate_netrc():
    """
    Validates if netrc file is present with the urs credentials in proper way 
    else prompt for urs user and password from user to create / setup netrc file 
    and used later redentails read from netrc file by any authentication
    """
    prompts = ['Enter NASA Earthdata Login Username: ',
            'Enter NASA Earthdata Login Password: ']

    # Determine the OS (Windows machines usually use an '_netrc' file)
    netrc_name = "_netrc" if system()=="Windows" else ".netrc"

    # Determine if netrc file exists, and if so, if it includes NASA Earthdata Login Credentials
    try:
        netrcDir = os.path.expanduser(f"~/{netrc_name}")
        netrc(netrcDir).authenticators(urs)[0]
        logger.info(f"netrc file is setup for {urs} already ...")

    # Below, create a netrc file and prompt user for NASA Earthdata Login Username and Password
    except FileNotFoundError:
        logger.info(f"netrc file not present. Creating via your user name / password for {urs}")
        homeDir = os.path.expanduser("~")
        Popen('touch {0}{2} | echo machine {1} >> {0}{2}'.format(homeDir + os.sep, urs, netrc_name), shell=True)
        Popen('echo login {} >> {}{}'.format(getpass(prompt=prompts[0]), homeDir + os.sep, netrc_name), shell=True)
        Popen('echo \'password {} \'>> {}{}'.format(getpass(prompt=prompts[1]), homeDir + os.sep, netrc_name), shell=True)
        # Set restrictive permissions
        Popen('chmod 0600 {0}{1}'.format(homeDir + os.sep, netrc_name), shell=True)

        # Determine OS and edit netrc file if it exists but is not set up for NASA Earthdata Login
    except TypeError:
        logger.info(f"netrc file is not setup for {urs}. Adding entry via your user name / password")
        homeDir = os.path.expanduser("~")
        Popen('echo machine {1} >> {0}{2}'.format(homeDir + os.sep, urs, netrc_name), shell=True)
        Popen('echo login {} >> {}{}'.format(getpass(prompt=prompts[0]), homeDir + os.sep, netrc_name), shell=True)
        Popen('echo \'password {} \'>> {}{}'.format(getpass(prompt=prompts[1]), homeDir + os.sep, netrc_name), shell=True)


def _format_session_credentials(temp_credentials):
    """Format credentials to be used by AWS session. Currently format for the RefreshableCredentials format
    Can be changed accordingly for different formats as needed later

    Args:
        temp_credentials (dict): Credentials from API
        {
            "accessKeyId": "ASsomeID",
            "secretAccessKey": "+XSomeID",
            "sessionToken": "FwoLongID",
            "expiration": "2022-07-28 16:55:32+00:00"
        }

    Returns:
        dict: {
            'access_key': '1234',
            'secret_key': 'abcd',
            'token': 'longtoken',
            'expiry_time': 'iso date string',
        }
    """
    return {
        'access_key': temp_credentials['accessKeyId'],
        'secret_key': temp_credentials['secretAccessKey'],
        'token': temp_credentials['sessionToken'],
        'expiry_time': temp_credentials['expiration'],
    }


def _get_new_temp_s3_credentials(s3_creds_endpoint):
    """This will get the temporary credentials for s3 access via call to API 
    This uses the EDL user / password from the netrc file validated / setup via _validate_netrc

    Returns:
        (dict): Return the credentials in format that will be needs by the RefreshableCredentials class from boto3
                Required credential format: {
                    'access_key': '1234',
                    'secret_key': 'abcd',
                    'token': 'longtoken',
                    'expiry_time': 'iso date string',
                }
    """
    logger.info(f'Getting new temporary credentials from AppEEARS API {s3_creds_endpoint}...')
    body = {}
    with requests.post(
            f"{s3_creds_endpoint}",
            json=body,
            auth=(
                netrc().authenticators(urs)[0],
                netrc().authenticators(urs)[2]
            )
        ) as resp:
        resp.raise_for_status()
        temp_credentials = resp.json()
        latest_creds = _format_session_credentials(temp_credentials)
        return latest_creds


async def _get_new_temp_s3_credentials_async(s3_creds_endpoint):
    """Just an async version of the _get_new_temp_s3_credentials
    that is needed by AioRefreshableCredentials , refresh_using param as it is
    credential = await self._refresh_using()
    https://github.com/aio-libs/aiobotocore/blob/88a43098b1194bf759581acc710ad5bdbdd99a96/aiobotocore/credentials.py#L337

    Returns:
        (dict): Return the credentials in format that will be needs by the RefreshableCredentials class from boto3
                Required credential format: {
                    'access_key': '1234',
                    'secret_key': 'abcd',
                    'token': 'longtoken',
                    'expiry_time': 'iso date string',
                }
    """
    return _get_new_temp_s3_credentials(s3_creds_endpoint)


def get_boto3_refreshable_session(s3_creds_endpoint, region_name='us-west-2'):
    """Get a refreshable session for the boto3 clients. This refreshable session will behind the scene
    calls the _get_credential function either to grab credentials via API or via prompt whenever it's near to expire

    That way user's don't have to look for expiration and refresh it themselves and they just create session once
    and call S3 API's later via boto3 which will take care of the session refresh automatically
    along with the refreshable credential object used by session (optional) 

    Returns:
        (tuple): (boto3_session, auto_refresh_credential_object (optional)):
                auto_refresh_credential_object is optional you can use that to refresh credentials manually too via
                auto_refresh_credential_object.get_frozen_credentials()
    """
    refreshable_credentials = RefreshableCredentials.create_from_metadata(
        metadata=_get_new_temp_s3_credentials(s3_creds_endpoint),
        refresh_using=partial(_get_new_temp_s3_credentials, s3_creds_endpoint),
        method="boto3_refreshable_credentials",
    )
    # If they aren't updated then boto refresh / generate the credentails for every API call
    refreshable_credentials._advisory_refresh_timeout = ADVISORY_REFRESH_TIMEOUT
    refreshable_credentials._mandatory_refresh_timeout = MANDATORY_REFRESH_TIMEOUT
    # Get botocore session
    session = get_session()
    # attach refreshable credentials current session
    session._credentials = refreshable_credentials
    session.set_config_variable("region", region_name)

    autorefresh_session = Session(botocore_session=session)

    return autorefresh_session


def get_s3fs_refreshable_session(s3_creds_endpoint, region_name='us-west-2'):
    """Get a refreshable session for the s3fs (S3 FileSystem) object. This refreshable session will behind the scene
    calls the creds_refresh_method function to grab credentials via API initially and 
    async_creds_refresh_method for refresh credentials later whenever it's near to expire

    s3fs uses aiobotocore and so need to use AioRefreshableCredentials that will get credentials intitially
    via creds_refresh_method and refresh_using call uses await pattern
    so need to use async_creds_refresh_method for that to work it correctly. 

    That way user's don't have to look for expiration and refresh it themselves and they just create session once
    and call S3 API's later via s3fs which will take care of the session refresh automatically
    along with the refreshable credential object used by session (optional) 

    Returns:
        (object): s3fs_aio_session: s3FS refreshable session
    """
    aio_refreshable_credentials = AioRefreshableCredentials.create_from_metadata(
        metadata=_get_new_temp_s3_credentials(s3_creds_endpoint),
        refresh_using=partial(_get_new_temp_s3_credentials_async, s3_creds_endpoint),
        method="s3fs_refreshable_credentials",
    )
    # If they aren't updated then boto will refresh / generate the credentails for every API call
    aio_refreshable_credentials._advisory_refresh_timeout = ADVISORY_REFRESH_TIMEOUT
    aio_refreshable_credentials._mandatory_refresh_timeout = MANDATORY_REFRESH_TIMEOUT
    # Get aiobotocore session as s3fs depends on aiobotocore
    aio_autorefresh_session = aio_get_session()
    # attach refreshable credentials current session
    aio_autorefresh_session._credentials = aio_refreshable_credentials
    aio_autorefresh_session.set_config_variable("region", region_name)

    return aio_autorefresh_session