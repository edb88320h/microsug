from ida_hexrays import *
import ida_idaapi


class deobf_visitor_t(minsn_visitor_t):
    def __init__(self):
        minsn_visitor_t.__init__(self)

    def visit_minsn(self):
        minsn = self.curins       
        if (minsn.opcode == m_mov or minsn.opcode == m_xdu) and minsn.l.dstr().find("$dword_") != -1:
            if not minsn.l.has_side_effects():
                minsn.l.make_number(0, 4)
        return 0


class deobfuscate_t(optinsn_t):
    def __init__(self):
        optinsn_t.__init__(self)
    def func(self, blk, ins, optflags):
        opt = deobf_visitor_t()
        ins.for_all_insns(opt)      
        return 0


class microsug_plugin_t(ida_idaapi.plugin_t):
    flags = ida_idaapi.PLUGIN_HIDE
    wanted_name = "Microsug"
    wanted_hotkey = ""
    comment = "A simple plugin to deobfuscate any dword-obfuscated code if this value is set to zero"
    help = ""
    def init(self):
        if init_hexrays_plugin():
            self.optimizer = deobfuscate_t()
            self.optimizer.install()
            return ida_idaapi.PLUGIN_KEEP 
    def term(self):
            self.optimizer.remove()
    def run(self):
            pass

def PLUGIN_ENTRY():
    return microsug_plugin_t()
