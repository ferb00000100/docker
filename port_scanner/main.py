import psycopg2
import botocore.exceptions
from concurrent.futures import ThreadPoolExecutor
# from logs import logger
# from time_it import timer
import get_db_data
# import get_aws_services
import assume_role
# import rumble_assets
# import scan_assets


# @timer
def get_saas_instance_ids():
    print('Getting Instances')
    instance_ids = []
    try:
        conn = psycopg2.connect(database=db_name, user=db_user, password=db_pwd, host=db_host, port=db_port)
    except Exception as err:
        print(err)
    else:
        cursor = conn.cursor()
        # cursor.execute("SELECT region FROM sc_assets")
        cursor.execute("SELECT service_provider, account_type, region, account_id, instanceid "
                       "FROM sc_assets ")

        for row in cursor:
            instance_details = {
                'service_provider': row[0],
                'account_type': row[1],
                'region': row[2],
                'account_id': row[3],
                'instanceid': row[4]
            }
            instance_ids.append(instance_details)

        for instance in instance_ids:
            print('Instance is', instance)
            region = instance['region']
            account = instance['account_id']
            instance_id = instance['instanceid']
            try:
                iso_security_enforce = assume_role.iso_security_enforce(account)
                print('iso_sec_enforce creds', iso_security_enforce)
                iso_enforce_credentials = assume_role.iso_enforce(account, region)
                print('iso_enforce creds', iso_enforce_credentials)
                # ec2Client = get_aws_services.get_ec2_client(region, iso_enforce_credentials)

                # response = ec2Client.describe_instances(
                #     InstanceIds=[
                #         instance_id,
                #     ],
                #     DryRun=False,
                # )
                # public_ip = response['Reservations'][0]['Instances'][0]['PublicIpAddress']
                # public_ip_list.append(public_ip)
            except botocore.exceptions.ClientError as error:
                if 'InvalidClientTokenId' in str(error):
                    print('Invalid Token', error)
                elif 'ExpiredToken' in str(error):
                    print('expired Toke', error)
            except KeyError as error:
                print('No public IP', error)
                pass
            except IndexError as error:
                print('End of Public IP List', error)
                pass

    return public_ip_list


if __name__ == '__main__':
    public_ip_list = []
    db_user = get_db_data.get_data('user')
    db_pwd = get_db_data.get_data('pwd')
    db_host = get_db_data.get_data('host')
    db_name = get_db_data.get_data('name')
    db_port = get_db_data.get_data('port')
    dev_sec_prod_acct = get_db_data.get_dev_sec_prod_acct()

    with ThreadPoolExecutor(max_workers=2) as executor:
        executor.map(get_saas_instance_ids(), timeout=None)
        executor.shutdown(wait=True)

    # logger.info('public ip list %s', public_ip_list)
    # rumble_assets.load_assets(public_ip_list)
    # scan_assets.scan_assets()
