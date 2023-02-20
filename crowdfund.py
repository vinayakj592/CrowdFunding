import smartpy as sp

class CrowdFunding(sp.Contract):
    def __init__(self,target,deadlineH,minContribution,admin):
        requestPARAM = sp.TRecord(
            description = sp.TString,
            recipient = sp.TAddress,
            value = sp.TNat,
            completed = sp.TBool,
            noOfVoters = sp.TNat
            # voters = sp.big_map(tkey = sp.TAddress, tvalue = sp.TBool)
        )
        
        self.init(
            # ob = CrowdFunding(sp.tez(5), sp.nat(5), sp.tez(1),admin.address)
        contributors = sp.big_map(tkey = sp.TAddress, tvalue = sp.TMutez),
        minContribution = minContribution,
        target = target,
        raisedAmount = sp.mutez(0),
        manager = admin,
        deadline = sp.now.add_hours(deadlineH),

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
        
        requestPARAM.description = params._description
        requestPARAM.recipient = params._recipient
        requestPARAM.value = params._value
        requestPARAM.completed = params._false
        requestPARAM.noOfVoters = 0

    @sp.entry_point
    def voteRequest(self,requestNo, _vote):

        #checks
        sp.verify(contributors[sp.sender]>sp.mutez(0), "You must be a contributor")
        requestPARAM.noOfVoters++
        

    @sp.add_test(name = "CrowdFund")
    def test():
        scenario = sp.test_scenario()

        admin = sp.test_account("admin")
        alice = sp.test_account("alice")
        bob = sp.test_account("bob")

        ob = CrowdFunding(sp.tez(5), sp.int(5), sp.tez(1),admin.address)
        scenario+=ob
        scenario += ob.receive().run(amount = sp.tez(1), sender = alice)
