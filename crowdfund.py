import smartpy as sp

class CrowdFunding(sp.Contract):
    def __init__(self,target,deadline,minContribution,admin):
        self.init(
            # ob = CrowdFunding(sp.tez(5), sp.nat(5), sp.tez(1),admin.address)
        contributors = sp.big_map(tkey = sp.TAddress, tvalue = sp.TNat),
        minContribution = minContribution,
        target = target,
        raisedAmount = sp.TNat,
        noOfContributions = sp.TNat,
        manager = admin,
        deadline = sp.TTimestamp,
            
        request = sp.TRecord(
            description = sp.TString,
            recipient = sp.TAddress,
            value = sp.TNat,
            completed = sp.TBool,
            noOfVoters = sp.TNat,
            #voters = sp.big_map(tkey = sp.TAddress, tvalue = sp.TBool)
        ),

        #requests = sp.big_map(tkey = sp.TNat, tvalue = request)
        )

    @sp.entry_point
    def receive(self):

        #checks
        sp.verify(sp.now<self.data.deadline, "Deadline has passed")
        sp.verify(sp.amount>= self.data.minContribution, "Minimun contribution not met")

        #storage updates
        self.data.noOfContributors = self.data.noOfContributors + 1;
        self.data.raisedAmount = self.data.raisedAmount + sp.amount
        self.data.contributors[sp.sender] = self.data.contributors[sp.sender] + sp.amount

    @sp.entry_point
    def refund(self):

        #checks
        sp.verify(sp.now>self.data.deadline & self.data.raisedAmount<self.data.target, "You are not eligible")
        sp.verify(self.data.contributors[sp.sender]>0)
        sp.send(sp.sender,self.data.contributors[sp.sender])
        self.data.contributors[sp.sender] = sp.tez(0)

    @sp.add_test(name = "CrowdFund")
    def test():
        scenario = sp.test_scenario()

        admin = sp.test_account("admin")
        alice = sp.test_account("alice")
        bob = sp.test_account("bob")

        ob = CrowdFunding(sp.tez(5), sp.nat(5), sp.tez(1),admin.address)
        scenario+=ob
        scenario += ob.receive().run(amount = sp.tez(1), sender = alice)

