class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        tmp1 = l1
        tmp2 = l2

        n1 = []
        while tmp1 != None:
            n1.append(tmp1.val)
            tmp1 = tmp1.next

        n2 = []
        while tmp2 != None:
            n2.append(tmp2.val)
            tmp2 = tmp2.next
       
        # make number
        n1 = sum([n*(10**i) for i, n in enumerate(n1)])
        n2 = sum([n*(10**i) for i, n in enumerate(n2)])
        twosum = n1 + n2

        answer = digits_to_listnode(list(str(twosum)[::-1]))
        #print_listnode(answer)
        return answer

def digits_to_listnode(digits):
    tmp = ListNode(digits[0])
    lnode = tmp
    for d in digits[1:]:
        tmp.next = ListNode(d)
        tmp = tmp.next

    return lnode

def print_listnode(lnode):
    while lnode != None:
        print('{} '.format(lnode.val), end='')
        lnode = lnode.next
    print()

l1 = digits_to_listnode([2,4,3])
l2 = digits_to_listnode([5,6,4])

l1 = digits_to_listnode([0])
l2 = digits_to_listnode([0])

l1 = digits_to_listnode([9,9,9,9,9,9,9])
l2 = digits_to_listnode([9,9,9,9])

sol = Solution()
sol.addTwoNumbers(l1, l2)
