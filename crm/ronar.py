#For printing out all users

# Import all the modules and Libraries
# import boto3
# from pprint import pprint #to get a print in a json format
# # Open Management Console
# aws_management_console = boto3.session.Session(profile_name="default")
# # Open IAM Console
# iam_console = aws_management_console.client(service_name="iam")
# # Use Boto3 Documentation to get more information (https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
# result = iam_console.list_users()
# for each_user in result['Users']:
#     # pprint(each_user['UserName'])

#########################################################################
#For printing out all EC2 instances

# Import all the modules and Libraries
# import boto3
# from pprint import pprint #to get a print in a json format
# # Open Management Console
# aws_management_console = boto3.session.Session(profile_name="default")
# # Open IAM Console
# ec2_console = aws_management_console.client(service_name="ec2")
# # Use Boto3 Documentation to get more information (https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
# result = ec2_console.describe_instances()['Reservations']

# for each_instance in result:
#     for value in each_instance['Instances']:
#         pprint(value['InstanceId'])

#########################################################################

# #Launching EC2 Instances

# import boto3

# aws_management_console = boto3.session.Session(profile_name="default")
# ec2_console = aws_management_console.client("ec2")

# response = ec2_console.run_instances(

#     ImageId = 'ami-0230bd60aa48260c6',
#     InstanceType = 't2.micro',
#     MaxCount = 1,
#     MinCount = 1
# )

#########################################################################

#Stopping EC2 Instances

# import boto3

# aws_management_console = boto3.session.Session(profile_name="default")
# ec2_console = aws_management_console.client(service_name="ec2")

# response = ec2_console.terminate_instances(
#     InstanceIds=['i-0083e73361a46dbb4']
# )