# -*- coding: utf-8 -*-
from __future__ import print_function

import json
import urllib
import boto3
import os
from botocore.exceptions import ClientError
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

print('Loading function')

s3 = boto3.client('s3')
snsclient = boto3.client('sns')
#snsTopicArn = "arn:aws:sns:us-west-2:789753010953:notifynewbuildprice"
#COMMASPACE = ', '

SENDER = "sergio.queiroz@buildnprice.io"
#RECIPIENT = ['vishramyadav@gmail.com', 'sergio.queiroz@buildnprice.io']
#API_GATEWAY_URL="https://cyh95hhhvj.execute-api.us-west-2.amazonaws.com/buildpricestageapi?filename="
#TO_RECIPIENT = "vishramyadav@gmail.com,sergio.queiroz@buildnprice.io"
AWS_REGION = "us-west-2"
SUBJECT = "Seu orçamento chegou!"
BODY_TEXT = "Hello,\r\nPlease see the attached file for a list of customers code prices.\n Please click here to BUY"
#BODY_HTML = """\
#<html>
#<head></head>
#<body>
#<h1>Hello!</h1>
#<p>Please see the attached file for a list of customers code prices.</p>
#<p>Please click here to <a href="API_GATEWAY_URL">BUY</a></p>
#</body>
#</html>
#"""
CHARSET = "utf-8"
sesClient = boto3.client('ses',region_name=AWS_REGION)


def lambda_handler(event, context):
    #print("Received event: " + json.dumps(event, indent=2))

    # Get the object from the event and show its content type
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = urllib.unquote_plus(event['Records'][0]['s3']['object']['key'].encode('utf8'))
    try:
        response = s3.get_object(Bucket=bucket, Key=key)
        print("CONTENT TYPE: " + response['ContentType'])
        #print(response)
        print(key)
        csvFileName=key[key.index('wrkflow_step5/')+14:]
        print(csvFileName)
        argsFileName=csvFileName[0:csvFileName.index('.')]
        print(argsFileName)
        API_GATEWAY_URL="https://cyh95hhhvj.execute-api.us-west-2.amazonaws.com/buildpricestageapi?filename="
        API_GATEWAY_URL=API_GATEWAY_URL+argsFileName+".json"
        
        BODY_HTML = """\
        <html>
        <head>
            <link rel="stylesheet" href="styles.css">
        </head>
        <body>
        <center>
            <table align="center" border="0" cellpadding="0" cellspacing="0" height="100%" width="100%" id="bodyTable">
            <tr>
            <td align="center" valign="top" id="bodyCell">
            <table border="0" cellpadding="0" cellspacing="0" width="100%">
            <tr>
            <td align="center" valign="top" id="templateHeader" data-template-container>
            <!--[if (gte mso 9)|(IE)]>
            <table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
            <tr> 
            <td align="center" valign="top" width="600" style="width:600px;">
            <![endif]-->
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
            <tr>
            <td valign="top" class="headerContainer">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageBlock" style="min-width:100%;">
            <tbody class="mcnImageBlockOuter">
            <tr>
            <td valign="top" style="padding:9px" class="mcnImageBlockInner">
            <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer" style="min-width:100%;">
            <tbody>
            <tr>
            <td class="mcnImageContent" valign="top" style="padding-right: 9px; padding-left: 9px; padding-top: 0; padding-bottom: 0; text-align:center;">
            <a href="https://www.buildnprice.io"><img align="center" alt="" src="https://gallery.mailchimp.com/fb0c986d2e5d0a8f082c8ddea/images/b8997b68-bbed-412f-99f6-8d086145810c.png" width="200" style="max-width:200px; padding-bottom: 0; display: inline !important; vertical-align: bottom;" class="mcnImage">
            </a>
            </td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </table>
            <!--[if (gte mso 9)|(IE)]>
            </td>
            </tr>
            </table>
            <![endif]-->
            </td>
            </tr>
            <tr>
            <td align="center" valign="top" id="templateBody" data-template-container>
            <!--[if (gte mso 9)|(IE)]>
            <table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
            <tr>
            <td align="center" valign="top" width="600" style="width:600px;">
            <![endif]-->
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
            <tr>
            <td valign="top" class="bodyContainer">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="min-width:100%;">
            <tbody class="mcnTextBlockOuter">
            <tr>
            <td valign="top" class="mcnTextBlockInner" style="padding-top:9px;">
            <!--[if mso]>
            <table align="left" border="0" cellspacing="0" cellpadding="0" width="100%" style="width:100%;">
            <tr>
            <![endif]-->
            
            <!--[if mso]>
            <td valign="top" width="600" style="width:600px;">
            <![endif]-->
            <table align="left" border="0" cellpadding="0" cellspacing="0" style="max-width:100%; min-width:100%;" width="100%" class="mcnTextContentContainer">
            <tbody>
            <tr>
            
            <td valign="top" class="mcnTextContent" style="padding-top:0; padding-right:18px; padding-bottom:9px; padding-left:18px;">
            
            <h3>Oi, seu orçamento chegou!</h3>
            
            <p>
            <span style="font-family:open sans,helvetica neue,helvetica,arial,sans-serif">Economizamos seu tempo e seu dinheiro!&nbsp; (｡♥‿♥｡)</span>
            </p>
            
            <p>
            <span style="font-family:open sans,helvetica neue,helvetica,arial,sans-serif">Em anexo, sua lista de compras com os melhores preços das melhores lojas de material de construção.</span>
            </p>
            
            </td>
            </tr>
            </tbody>
            </table>
            <!--[if mso]>
            </td>
            <![endif]-->
            
            <!--[if mso]>
            </tr>
            </table>
            <![endif]-->
            </td>
            </tr>
            </tbody>
            </table>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnImageBlock" style="min-width:100%;">
            <tbody class="mcnImageBlockOuter">
            <tr>
            <td valign="top" style="padding:9px" class="mcnImageBlockInner">
            <table align="left" width="100%" border="0" cellpadding="0" cellspacing="0" class="mcnImageContentContainer" style="min-width:100%;">
            <tbody>
            <tr>
            <td class="mcnImageContent" valign="top" style="padding-right: 9px; padding-left: 9px; padding-top: 0; padding-bottom: 0; text-align:center;">
            
            
            <img align="center" alt="" src="https://gallery.mailchimp.com/fb0c986d2e5d0a8f082c8ddea/images/846becba-69dd-4828-a3dc-02faa410fa74.png"
            width="465" style="max-width:465px; padding-bottom: 0; display: inline !important; vertical-align: bottom;"
            class="mcnImage">
            
            
            </td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnDividerBlock" style="min-width:100%;">
            <tbody class="mcnDividerBlockOuter">
            <tr>
            <td class="mcnDividerBlockInner" style="min-width:100%; padding:18px;">
            <table class="mcnDividerContent" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;">
            <tbody>
            <tr>
            <td>
            <span></span>
            </td>
            </tr>
            </tbody>
            </table>
            <!--            
            <td class="mcnDividerBlockInner" style="padding: 18px;">
            <hr class="mcnDividerContent" style="border-bottom-color:none; border-left-color:none; border-right-color:none; border-bottom-width:0; border-left-width:0; border-right-width:0; margin-top:0; margin-right:0; margin-bottom:0; margin-left:0;" />
            -->
            </td>
            </tr>
            </tbody>
            </table>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnButtonBlock" style="min-width:100%;">
            <tbody class="mcnButtonBlockOuter">
            <tr>
            <td style="padding-top:0; padding-right:18px; padding-bottom:18px; padding-left:18px;" valign="top" align="center" class="mcnButtonBlockInner">
            <table border="0" cellpadding="0" cellspacing="0" class="mcnButtonContentContainer" style="border-collapse: separate !important;border-radius: 3px;background-color: #00ADD8;">
            <tbody>
            <tr>
            <td align="center" valign="middle" class="mcnButtonContent" style="font-family: &quot;Open Sans&quot;, &quot;Helvetica Neue&quot;, Helvetica, Arial, sans-serif; font-size: 18px; padding: 18px;">
            <a class="mcnButton " title="Quero comprar!" href="{API_GATEWAY_URL}" target="_self" style="font-weight: bold;letter-spacing: -0.5px;line-height: 100%;text-align: center;text-decoration: none;color: #FFFFFF;">Quero comprar!</a>
            </td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </table>
            <!--[if (gte mso 9)|(IE)]>
            </td>
            </tr>
            </table>
            <![endif]-->
            </td>
            </tr>
            <tr>
            <td align="center" valign="top" id="templateFooter" data-template-container>
            <!--[if (gte mso 9)|(IE)]>
            <table align="center" border="0" cellspacing="0" cellpadding="0" width="600" style="width:600px;">
            <tr>
            <td align="center" valign="top" width="600" style="width:600px;">
            <![endif]-->
            <table align="center" border="0" cellpadding="0" cellspacing="0" width="100%" class="templateContainer">
            <tr>
            <td valign="top" class="footerContainer">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowBlock" style="min-width:100%;">
            <tbody class="mcnFollowBlockOuter">
            <tr>
            <td align="center" valign="top" style="padding:9px" class="mcnFollowBlockInner">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentContainer" style="min-width:100%;">
            <tbody>
            <tr>
            <td align="center" style="padding-left:9px;padding-right:9px;">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width:100%;" class="mcnFollowContent">
            <tbody>
            <tr>
            <td align="center" valign="top" style="padding-top:9px; padding-right:9px; padding-left:9px;">
            <table align="center" border="0" cellpadding="0" cellspacing="0">
            <tbody>
            <tr>
            <td align="center" valign="top">
            <!--[if mso]>
            <table align="center" border="0" cellspacing="0" cellpadding="0">
            <tr>
            <![endif]-->
            
            <!--[if mso]>
            <td align="center" valign="top">
            <![endif]-->
            
            
            <table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;">
            <tbody>
            <tr>
            <td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
            <tbody>
            <tr>
            <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
            <table align="left" border="0" cellpadding="0" cellspacing="0" width="">
            <tbody>
            <tr>
            
            <td align="center" valign="middle" width="24" class="mcnFollowIconContent">
            <a href="https://www.buildnprice.io" target="_blank">
            <img src="https://cdn-images.mailchimp.com/icons/social-block-v2/outline-light-link-48.png"
            style="display:block;" height="24" width="24" class="">
            </a>
            </td>
            
            
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            
            <!--[if mso]>
            </td>
            <![endif]-->
            
            <!--[if mso]>
            <td align="center" valign="top">
            <![endif]-->
            
            
            <table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;">
            <tbody>
            <tr>
            <td valign="top" style="padding-right:10px; padding-bottom:9px;" class="mcnFollowContentItemContainer">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
            <tbody>
            <tr>
            <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
            <table align="left" border="0" cellpadding="0" cellspacing="0" width="">
            <tbody>
            <tr>
            
            <td align="center" valign="middle" width="24" class="mcnFollowIconContent">
            <a href="http://www.facebook.com/buildnprice" target="_blank">
            <img src="https://cdn-images.mailchimp.com/icons/social-block-v2/outline-light-facebook-48.png"
            style="display:block;" height="24" width="24" class="">
            </a>
            </td>
            
            
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            
            <!--[if mso]>
            </td>
            <![endif]-->
            
            <!--[if mso]>
            <td align="center" valign="top">
            <![endif]-->
            
            
            <table align="left" border="0" cellpadding="0" cellspacing="0" style="display:inline;">
            <tbody>
            <tr>
            <td valign="top" style="padding-right:0; padding-bottom:9px;" class="mcnFollowContentItemContainer">
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnFollowContentItem">
            <tbody>
            <tr>
            <td align="left" valign="middle" style="padding-top:5px; padding-right:10px; padding-bottom:5px; padding-left:9px;">
            <table align="left" border="0" cellpadding="0" cellspacing="0" width="">
            <tbody>
            <tr>
            
            <td align="center" valign="middle" width="24" class="mcnFollowIconContent">
            <a href="http://www.twitter.com/buildnprice" target="_blank">
            <img src="https://cdn-images.mailchimp.com/icons/social-block-v2/outline-light-twitter-48.png"
            style="display:block;" height="24" width="24" class="">
            </a>
            </td>
            
            
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            
            <!--[if mso]>
            </td>
            <![endif]-->
            
            <!--[if mso]>
            </tr>
            </table>
            <![endif]-->
            </td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </tbody>
            </table>
            
            </td>
            </tr>
            </tbody>
            </table>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnDividerBlock" style="min-width:100%;">
            <tbody class="mcnDividerBlockOuter">
            <tr>
            <td class="mcnDividerBlockInner" style="min-width:100%; padding:18px;">
            <table class="mcnDividerContent" border="0" cellpadding="0" cellspacing="0" width="100%" style="min-width: 100%;border-top: 2px solid #505050;">
            <tbody>
            <tr>
            <td>
            <span></span>
            </td>
            </tr>
            </tbody>
            </table>
            <!--            
            <td class="mcnDividerBlockInner" style="padding: 18px;">
            <hr class="mcnDividerContent" style="border-bottom-color:none; border-left-color:none; border-right-color:none; border-bottom-width:0; border-left-width:0; border-right-width:0; margin-top:0; margin-right:0; margin-bottom:0; margin-left:0;" />
            -->
            </td>
            </tr>
            </tbody>
            </table>
            <table border="0" cellpadding="0" cellspacing="0" width="100%" class="mcnTextBlock" style="min-width:100%;">
            <tbody class="mcnTextBlockOuter">
            <tr>
            <td valign="top" class="mcnTextBlockInner" style="padding-top:9px;">
            <!--[if mso]>
            <table align="left" border="0" cellspacing="0" cellpadding="0" width="100%" style="width:100%;">
            <tr>
            <![endif]-->
            
            <!--[if mso]>
            <td valign="top" width="600" style="width:600px;">
            <![endif]-->
            <table align="left" border="0" cellpadding="0" cellspacing="0" style="max-width:100%; min-width:100%;" width="100%" class="mcnTextContentContainer">
            <tbody>
            </tbody>
            </table>
            <!--[if mso]>
            </td>
            <![endif]-->
            
            <!--[if mso]>
            </tr>
            </table>
            <![endif]-->
            </td>
            </tr>
            </tbody>
            </table>
            </td>
            </tr>
            </table>
            <!--[if (gte mso 9)|(IE)]>
            </td>
            </tr>
            </table>
            <![endif]-->
            </td>
            </tr>
            </table>
            <!-- // END TEMPLATE -->
            </td>
            </tr>
            </table>
	    </center>
        </body>
        </html>
        """.format(API_GATEWAY_URL=API_GATEWAY_URL)
        
        fileContent=response['Body'].read().decode('utf-8')
        print(fileContent)
        emailList=getSNSSubscribtionEmails(argsFileName)
        emailList.append('sergio.queiroz@buildnprice.io')
        print(emailList);
        #RECIPIENT=emailList
        #sendSNSNotification();
        sendEmailWithAttachment(fileContent,csvFileName,emailList,BODY_HTML)
        return response['ContentType']
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e
        
def getSNSSubscribtionEmails(fileName):
    emailList=[]
    try:
        snsTopicArn = "arn:aws:sns:us-west-2:789753010953:"+fileName
        snsRes = snsclient.list_subscriptions_by_topic(
        TopicArn=snsTopicArn
    )
    
        for record in snsRes['Subscriptions']:
            if record['Protocol'] == 'email':
                emailList.append(record['Endpoint'])
    except Exception as e:
        print(e)
        print('Error occured while getting email from sns object')
    return emailList

def sendEmailWithAttachment(fileContent,csvFileName,RECIPIENT,BODY_HTML):
    
    msg = MIMEMultipart('mixed')
    msg['Subject'] = SUBJECT 
    msg['From'] = SENDER 
    msg['To'] = ",".join(RECIPIENT) 

    msg_body = MIMEMultipart('alternative')
    textpart = MIMEText(BODY_TEXT.encode(CHARSET), 'plain', CHARSET)
    htmlpart = MIMEText(BODY_HTML.encode(CHARSET), 'html', CHARSET)

    #msg_body.attach(textpart)
    msg_body.attach(htmlpart)

    att = MIMEApplication(fileContent)

    att.add_header('Content-Disposition','attachment',filename=csvFileName)

    msg.attach(msg_body)

    msg.attach(att)
    print(msg)
    try:
    
        sesResponse = sesClient.send_raw_email(
        Source=SENDER,
        Destinations=RECIPIENT
    ,
        RawMessage={
            'Data':msg.as_string(),
        }
        #,ConfigurationSetName=CONFIGURATION_SET
    )

    except ClientError as e:
        print(e.response['Error']['Message'])
    
    print("Email sent! Message ID:"),
    #print(response['ResponseMetadata']['RequestId'])
    
def sendSNSNotification():
    response = snsclient.publish(
    TopicArn=snsTopicArn,
    Message='Please see the latest list of customers code prices',
    Subject='customers code prices',
    MessageStructure='string'
)