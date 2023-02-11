# <p align="center">**Automation Diagram**</p>

## **Start Up**
| Phase | Environment | Server Type |
|-------|-------------|-------------|
| Phase 1 | Development, Test, Pre-Production | Database |
| Phase 2 | Development | Application |
| Phase 3 | Test | Application |
| Phase 4 | Pre-Production | Application |

[**Start EC2 Flow Diagram**](/source/images/lambda_startup_diagram.PNG)
<img src="/source/images/lambda_startup_diagram.PNG">

## **Shutdown**
| Phase | Environment | Server Type|
|-------|-------------|------------|
| Phase 1 | Development | Application |
| Phase 2 | Test | Application |
| Phase 3 | Pre-Production | Application |
| Phase 4 | Development | Database |
| Phase 5 | Test | Database |
| Phase 6 | Pre-Production | Database |

[**Stop EC2 Flow Diagram**](/source/images/lambda_startup_diagram.PNG)
<img src="/source/images/lambda_shutdown_diagram.png">
