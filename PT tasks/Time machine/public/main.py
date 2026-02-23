import sys


class VM(object):

    def __init__(self, inp):
        self.stack = []
        self.skip = 0
        self.ok = False
        self.input = inp
        self.regs = {'r1': 0, 
                     'r2': 0,
                     'r3': 0,
                     'r4': 0,
                     'r5': 0,
                     'r6': 0,
                     'r7': 0,
                     'r8': 0
                    }

    def skippable(f):

        def inner(self, *args):
            if self.skip == 0:
                return f(self, *args)
            else:
                self.skip -= 1
                return self

        return inner

    @skippable
    def add(self,r1, r2, r3):
        self.regs[r1] = (self.regs[r2] + self.regs[r3]) & 0xff
        return self

    @skippable
    def skip_n(self, count):
        self.skip = count
        return self

    @skippable
    def sub(self, r1, r2, r3):
        self.regs[r1] = (self.regs[r2] - self.regs[r3]) & 0xff
        return self

    @skippable
    def load(self, r1, idx):
        if idx >= len(self.input):
            self.skip = 0xdfffff
        self.regs[r1] = ord(self.input[idx])
        return self

    @skippable
    def mul(self, r1, r2, r3):
        self.regs[r1] = (self.regs[r2] * self.regs[r3]) & 0xff
        return self

    @skippable
    def set_ok(self):
        self.ok = True
        return self

    @skippable
    def comp_critical(self, r1, r2):
        if self.regs[r1] != self.regs[r2]:
            self.skip = 0xdead
        return self

    @skippable
    def load_const(self, r1, const):
        self.regs[r1] = const
        return self


if len(sys.argv) < 2:
    print("Usage <flag>")
    exit(-0xcafebabe)

inp = sys.argv[1]
vm = VM(inp)

if len(inp) != 14:
    print("Nope. Invalid Length")
    exit(0)

vm = vm.load_const('r6', 86).load('r5', 0).comp_critical('r5','r6').load_const('r1', 23).add('r6', 'r6', 'r1').load('r5', 1).comp_critical('r6', 'r5').load_const('r2', 14).sub('r7', 'r6','r2').load('r5', 2).comp_critical('r7','r5').load_const('r3', 49).load('r5', 3).comp_critical('r3','r5').load_const('r1', 29).load_const('r3', 53).mul('r6', 'r1', 'r3').mul('r6', 'r6', 'r3').load('r5', 4).comp_critical('r5', 'r6').load('r5', 5).comp_critical('r7','r5').load_const('r1', 110).load('r5', 6).comp_critical('r1', 'r5').load_const('r4', 6).add('r5','r1','r4').load('r6', 8).comp_critical('r5','r6').load_const('r2', 48).load('r1',7).comp_critical('r1','r2').load('r8',9).comp_critical('r7','r8').load_const('r1', 159).mul('r1','r7','r1').load_const('r2',103).add('r1','r1','r2').load('r5',10).comp_critical('r1', 'r5').load_const('r4', 35).load_const('r1',29).add('r7', 'r1','r4').load('r5', 11).comp_critical('r7', 'r5').load('r5', 12).load_const('r1', 0).load_const('r2', 44).sub('r5','r5','r2').load_const('r2', 38).sub('r5', 'r5','r2').comp_critical('r1','r5').load_const('r7',68).load('r5', 13).comp_critical('r7', 'r5').set_ok()
if vm.ok == True:
    print("YEP!")
else:
    print("Nope. Invalid flag")
