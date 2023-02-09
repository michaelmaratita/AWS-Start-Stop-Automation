# <img src="source/images/logos/CW_alert.png" width=10% height=10%> Creating CloudWatch EC2 Alarms

**1**. Select the **CloudWatch** service

**2**. Under **CloudWatch** > Expand **Alarms** > Select **All alarms**

<img src="/source/images/cloudwatch/cw_1.PNG">

**3**. Select **Create alarm**
<img align="center"src="/source/images/cloudwatch/cw_2.png">

**4**. Under **Metric** > Select **`Select metric`**

**5**. Under **Browse** > **Metrics** > Expand **AWS namespaces**
- Select the **`EC2`** Option
<img src="/source/images/cloudwatch/cw_3.png">

**6**. Select **`Per-Instance Metrics`**
<img src="/source/images/cloudwatch/cw_4.png">
- Search for the EC2 Instance name, e.g. **AEDVECOMWSSBM01**
- Select the Appropriate Metric associated with the EC2 instace, e.g. **StatusCheckFailed**
- Select **`Select metric`**
<img src="/source/images/cloudwatch/cw_5.png">

**7**. Under **Conditions** Pane > Select **Static**
    - Select **Greater/Equal** 
    - Enter Value **1**
    - Select **Next**
<img src="/source/images/cloudwatch/cw_6.PNG" width=50%>

**8**. Under **Notification**
    - Select **In alarm** radio button
    - Select **Select an existing SNS topic** radio button
    - From the dropdown, select the apporpriate SNS topic, e.g. **ecom_cloudwatch_snsalerts**
    - Select **Next**
<img src="/source/images/cloudwatch/cw_8.png" width=70%>

**9**. Enter **Alarm name**, e.g. SERVERNAME- StatusCheckFailed
    - Select **Next**
<img src="/source/images/cloudwatch/cw_9.PNG" width=70%>

**10**. Validate Alarm settings
    - Select   <img src="/source/images/cloudwatch/cw_10.PNG">
