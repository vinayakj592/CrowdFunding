![banner](https://user-images.githubusercontent.com/85495019/220703960-bb7221c2-abd8-4e68-8c97-9177d1427197.png)

![GitHub last commit](https://img.shields.io/github/last-commit/vinayakj592/CrowdFunding) 

This is a Tezos blockchain-based crowdfunding contract developed using the SmartPy smart contract development platform. It enables the creation of crowdfunding campaigns, where backers can pledge funds and the campaign creator can submit requests to withdraw funds for specific purposes. The withdrawal request is then subjected to a voting process by the backers, which takes place if the funding goal is met within a specified time period.

## Entry Points

 - **receive()**\
 The "receive()" entry point of the contract enables users to make pledges towards a crowdfunding campaign by depositing their funds into the contract.
 
 - **refund()**\
In the event that a crowdfunding campaign's funding goal is not met within the specified deadline, the "refund()" entry point of the contract enables contributors to    withdraw their pledged funds.

- **createRequest()**\
With the "createRequest()" entry point of the contract, the campaign creator can request the transfer of funds for a specific purpose by providing a description of the request, the address of the recipient, and the amount to be transferred.

- **voteRequest()**\
By using the "voteRequest()" entry point of the contract, contributors can cast their votes on a request created by the campaign creator. The voting process involves specifying the request number and indicating a "True" or "False" vote.

- **makePayment()**\
If over 50% of the contributors vote "True" for a specific request, the campaign creator can use the "makePayment()" entry point to transfer funds to the specified recipient by entering the request number into the contract. This allows the campaign creator to execute the request and disburse funds for the intended purpose.

## Contract

Address : KT1Msor4MoSNjxaKHGK9ViRsyUKY7cD4XPRj

[Explore with TzKT](https://ghostnet.tzkt.io/KT1Msor4MoSNjxaKHGK9ViRsyUKY7cD4XPRj/operations/)

## Contributing

Contributions to this project are welcome! If you would like to contribute, please fork the repository and submit a pull request with your changes.

## Lisence

This project is licensed under the MIT License - see the `LICENSE` file for details.
