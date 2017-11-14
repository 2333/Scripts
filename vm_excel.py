import xlrd
import xlwt
import re


# from datetime
def openfile(filename):
    try:
        data = xlrd.open_workbook(filename)
        return data
    except Exception as e:
        print(str(e))


def vmxlrd(filename):
    book = openfile(filename)
    print(book)
    # print("Worksheet name(s): ", book.sheet_names()[0])
    sh = book.sheet_by_index(0)

    print('book.nsheets', book.nsheets)
    print('sh.name:', sh.name, 'sh.nrows:', sh.nrows, 'sh.ncols:', sh.ncols)
    # print('A1:', sh.cell_value(rowx=0, colx=0))
    # 如果A3的内容为中文
    # print('A2:', sh.cell_value(167, 0))

# 1214 comment
    # name = re.match(r'[T|B|P]\-(\w+?)\-(\w+?)\-', sh.cell_value(0, 0))
    # print(name.group(1), name.group(2))
    # n = 0
    # lists = []
    # print(sh.col)
    # while n < sh.nrows:
    #     name = re.search(r"[TBPt]\-([^\-]*)(\-([^\-]*)|$)", sh.cell_value(n, 0))
    #     if name is None:
    #         lists.append((0, 0))
    #     else:
    #         print(n, ': ', sh.cell_value(n, 0), '\t', name.group(1), '\t', name.group(3))
    #         lists.append([sh.cell_value(n, 0), name.group(1), name.group(3)])
    #     n += 1
    # print(lists[0][2])
    # vmlists = cmp_vmname('vmdata.xlsx', 'syslist.xlsx', lists)
    # a = open("lists.txt", 'w')
    # for vm in vmlists:
    #     print(vm)
    #     for v in vm:
    #         a.write(str(v))
    #         a.write('\t')
    #     a.write('\n')
    # a.close()
    #vmxlwt('vmdetail.xls', vmlists)
    take_vm_name(sh)


def take_vm_name(sh):
    with open("testVM_names.txt", "w") as f:
        for i in range(1, sh.nrows):
            hostname = sh.cell_value(i, 1)
            namesplit = hostname.split('-')
            print(namesplit)
            if namesplit[-1].isdigit():
                if len(namesplit) >= 2:
                    print(namesplit[-2])
                    f.write(hostname + "\t" + namesplit[-2] + "\n")
            else:
                if len(namesplit) >= 3:
                    print(namesplit[-3])
                    f.write(hostname + "\t" + namesplit[-3] + "\n")


def cmp_vmname(vmdata, syslist, lists):
    vmdataxl = openfile(vmdata)
    syslistxl = openfile(syslist)
    vmdatash = vmdataxl.sheet_by_index(0)
    syslistsh = syslistxl.sheet_by_index(0)

    sysdict = {}
    i = 0
    while i < syslistsh.nrows:
        sysdict[syslistsh.cell_value(i, 1)] = syslistsh.cell_value(i, 0)
        i += 1

    for listname in lists:
        n = 0
        while n < vmdatash.nrows:
            vmname = vmdatash.cell_value(n, 0)
            name = re.search(r"[TBPt]\-([^\-]*)(\-([^\-]*)|$)", vmname)
            if listname[0] == vmname:
                listname += vmdatash.row_values(n, 1, 4)
                break
            elif hasattr(name, "group") and listname[1] == name.group(1) and listname[2] == name.group(3):
                listname += vmdatash.row_values(n, 1, 4)
                break
            n += 1
        if listname[1] in sysdict:
            listname.append(sysdict.get(listname[1]))
    return lists


def vmxlwt(filename, lists):
    book = xlwt.Workbook()
    sheet1 = book.add_sheet('vm_detail')
    for i in range(len(lists)):
        j = 0
        for con in lists[i]:
            sheet1.write(i, j, con)
            j += 1
    book.save(filename)


if __name__ == '__main__':
    # vmxlrd("vmware.xls")
    vmxlrd("D:\kvm_list\\t-vm.xls")
