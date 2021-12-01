class stacks2:
    def __init__(self,size):
        self.size=size
        self.array=[None] *size
        self.top1=-1
        self.top2=self.size
    def push1(self,data):
        if self.top1<self.top2-1:
            self.top1=self.top1+1
            self.array[self.top1]=data
        else:
            print("stack overflow")
    def push2(self,data):
        if self.top1<self.top2-1:
            self.top2=self.top2-1
            self.array[self.top2]=data
        else:
            print("stack overflow")
    def pop1(self):
        if self.top1>=0:
            x=self.array[self.top1]
            self.top1-=1
            return x
        else:
            print("stack underflow") 
            return     
    def pop2(self):
        if self.top2<self.size:
            x=self.array[self.top2]
            self.top2+=1
            return x
        else:
            print("stack underflow")
            return
if __name__=="__main__":
    twostacks=stacks2(8)
    twostacks.push1(1)
    twostacks.push1(2)
    twostacks.push1(3)
    twostacks.push2(4)
    twostacks.push2(5)
    twostacks.push2(6)
    twostacks.push1(7)
    twostacks.push1(0)
    print(twostacks.array)
    print("popped element from stack1 %d"%twostacks.pop1())
    print("popped element from stack1 %d"%twostacks.pop2())
    twostacks.push2(8)
    twostacks.push1(9)
    print(twostacks.array)
