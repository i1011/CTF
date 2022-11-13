import angr
import claripy
def main():
    elf = "./backup_babycmp_chall.baby"
    flag = claripy.BVS('FLAG', 8 * 0x30)

    proj = angr.Project(elf)
    state = proj.factory.entry_state(args=[elf, flag])
    sim = proj.factory.simgr(state)
    addr = 0x4012cc
    sim.explore(find=addr)
    for s in sim.found:
        print(s.solver.eval(flag, cast_to=bytes))
if __name__== "__main__":
    main()