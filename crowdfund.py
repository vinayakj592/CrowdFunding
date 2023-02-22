import smartpy as sp

class CrowdFunding(sp.Contract):
    def __init__(self,target,deadlineH,minContribution,admin):
        requestPARAM = sp.TRecord(
            description = sp.TString,
            recipient = sp.TAddress,
            value = sp.TNat,
            completed = sp.TBool,
            noOfVoters = sp.TNat
        )
        
        self.init(
        contributors = sp.map(tkey = sp.TAddress, tvalue = sp.TMutez),
        minContribution = minContribution,
        target = target,
        raisedAmount = sp.mutez(0),
        manager = admin,
        deadline = sp.now.add_hours(deadlineH),
        reqid = sp.nat(0),
        requests = sp.big_map(tkey = sp.TNat, tvalue = requestPARAM),
        voters = sp.big_map(tkey = sp.TRecord(id = sp.TNat , add= sp.TAddress) , tvalue = sp.TBool)  
        )

    @sp.entry_point
    def receive(self):

        #checks
        sp.verify(sp.now<self.data.deadline, "Deadline has passed")
        sp.verify(sp.amount>= self.data.minContribution, "Minimun contribution not met")

        #storage updates
        self.data.raisedAmount = self.data.raisedAmount + sp.amount
        sp.if self.data.contributors.contains(sp.sender):
            self.data.contributors[sp.sender] = self.data.contributors[sp.sender] + sp.amount
        sp.else:
            self.data.contributors[sp.sender] = sp.amount
            
    @sp.entry_point
    def refund(self):

        #checks
        sp.verify(sp.now>self.data.deadline , "You are not eligible")
        sp.verify(self.data.raisedAmount<self.data.target , "You are not eligible")
        sp.verify(self.data.contributors[sp.sender] > sp.mutez(0))
        sp.send(sp.sender,self.data.contributors[sp.sender])
        self.data.contributors[sp.sender] = sp.tez(0)

    @sp.entry_point
    def createRequest(self,params):

        #checks
        sp.verify(sp.sender == self.data.manager, "Only Manager can create requests")
        self.data.requests[self.data.reqid] = sp.record(
            description =  params._description,
            recipient = params._recipient,
            value = params._value,
            completed = sp.bool(False),
            noOfVoters = sp.nat(0))
        self.data.reqid = self.data.reqid+1

    @sp.entry_point
    def voteRequest(self,requestNo, _vote):

        #checks
        sp.verify(self.data.contributors[sp.sender]>sp.mutez(0), "You must be a contributor")
        sp.verify(self.data.requests.contains(requestNo),"Request not available")
        sp.verify(~self.data.voters.contains(sp.record(id = requestNo, add = sp.sender)), "Already voted")
        self.data.voters[sp.record(id = requestNo, add = sp.sender)] = _vote
        sp.if _vote == sp.bool(True) :
            self.data.requests[requestNo].noOfVoters = self.data.requests[requestNo].noOfVoters+1

    @sp.entry_point
    def makePayment(self, requestNo):

        #checks
        sp.verify(sp.sender == self.data.manager, "Only Manager can create requests")
        sp.verify(self.data.requests[requestNo].noOfVoters > (sp.len(self.data.contributors)//2) , "Minimun voters requriment not met")
        sp.verify(self.data.requests[requestNo].completed == False, "Request already completed")
        sp.send(self.data.requests[requestNo].recipient, sp.utils.nat_to_mutez(self.data.requests[requestNo].value))
        self.data.requests[requestNo].completed = True

    @sp.add_test(name = "CrowdFund")
    def test():
        scenario = sp.test_scenario()

        admin = sp.test_account("admin")
        alice = sp.test_account("alice")
        bob = sp.test_account("bob")
        jack = sp.test_account("jack")
        mike = sp.test_account("mike")

        ob = CrowdFunding(sp.tez(5), sp.int(5), sp.tez(1),admin.address)
        scenario+=ob
        scenario += ob.receive().run(amount = sp.tez(1), sender = alice)
        scenario += ob.receive().run(amount = sp.tez(2), sender = bob)
        scenario += ob.receive().run(amount = sp.tez(1), sender = jack)
        scenario += ob.receive().run(amount = sp.tez(2), sender = mike, now = sp.timestamp(180001),valid  = False)

        scenario += ob.refund(
        ).run(sender = alice,valid = False)

        scenario += ob.createRequest(
            _description = "Want money for raw materials",
            _recipient = bob.address,
            _value = 2000000
        ).run(sender = admin)

        scenario += ob.createRequest(
            _description = "Want money for shopping",
            _recipient = bob.address,
            _value = 2000000
        ).run(sender = bob, valid = False)
        
        scenario += ob.voteRequest(
            requestNo = sp.nat(0),
            _vote = True
        ).run(sender = alice)

        scenario += ob.voteRequest(
            requestNo = sp.nat(0),
            _vote = True
        ).run(sender = bob)

        scenario += ob.voteRequest(
            requestNo = sp.nat(0),
            _vote = True
        ).run(sender = bob,valid = False)

        scenario += ob.voteRequest(
            requestNo = sp.nat(0),
            _vote = False
        ).run(sender = jack)

        scenario += ob.makePayment(
            sp.nat(0)
        ).run(sender = admin)
