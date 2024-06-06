#!/usr/bin/env python3
import sys
import re
import json
import os

def main():
    need_help = False
    defines = []
    skip_next = 0
    prog_args = []
    for i, a in enumerate(sys.argv[1:], 1):
        if skip_next > 0:
            skip_next -= 1
            continue
        if a == "--help" or a == "-h":
            need_help = True
        if a == "-D":
            defines.append(sys.argv[i + 1])
            skip_next = 1
        elif a.startswith("-D"):
            defines.append(a[2:])
        else:
            prog_args.append(a)

    defines = [d.split("=")[0] for d in defines]
    
    if len(prog_args) < 2 or need_help:
        print("Usage: {} <demo_data.json> <assets.json> [-D <symbol>] > <demo_data.c>".format(sys.argv[0]))
        sys.exit(0 if need_help else 1)

    with open(prog_args[0], "r") as file:
        descr = json.loads(re.sub(r"/\*[\w\W]*?\*/", "", file.read()))

    with open(prog_args[1], "r") as file:
        assets = json.loads(re.sub(r"/\*[\w\W]*?\*/", "", file.read()))

    table = []
    for item in descr["table"]:
        if not "ifdef" in item or any(d in defines for d in item["ifdef"]):
            table.append(item)

    demofiles = []
    for item in descr["demofiles"]:
        if not "ifdef" in item or any(d in defines for d in item["ifdef"]):
            demofiles.append(item)

    structdef = ["u32 numEntries;",
                 "const void *addrPlaceholder;",
                 "struct OffsetSizePair entries[" + str(len(table)) + "];"]
    structobj = [str(len(table)) + ",",
                 "NULL,"]

    structobj.append("{")
    for item in table:
        offset_to_data = "offsetof(struct DemoInputsObj, " + item["demofile"] + ")"
        size = "sizeof(gDemoInputs." + item["demofile"] + ")"
        if "extraSize" in item:
            size += " + " + str(item["extraSize"])
        structobj.append("{" + offset_to_data + ", " + size + "},")
    structobj.append("},")

    for item in demofiles:
        demosize=assets["assets/demos/%s.bin" % item["name"]][0]
        structdef.append("u8 " + item["name"] + "[" + str(demosize) + "];")
        structobj.append("{},")

    print("#include \"types.h\"")
    print("#include <stddef.h>")
    print("")

    print("struct DemoInputsObj {")
    for s in structdef:
        print(s)
    print("} gDemoInputs = {")
    for s in structobj:
        print(s)
    print("};")

    print('')


    print('int demo_data_load(){')
    print('    fs_file_t *file;')
    print('    int size;')
    print('    printf("Loading demo data\\n");')



    for item in demofiles:
        demoname=item["name"]
        print('    printf("Loading %s.bin\\n");' % demoname)
        print('    file = fs_open("./demos/%s.bin");' % demoname)
        print('    if (file == NULL) {')
        print('        printf("Cannot open file\\n");')
        print('    }')
        print('    if((size = fs_read(file, gDemoInputs.%s, sizeof(gDemoInputs.%s))) != sizeof(gDemoInputs.%s)){' % (demoname,demoname,demoname))
        print('        printf("Warning: expecting %' + 'd bytes but only got %' + 'd.\\n",sizeof(gDemoInputs.%s),size);' % demoname)
        print('    }')
        print('    printf("%' + 'd bytes read\\n", size);')
        print('    fs_close(file);')
        print('')
    
    print('    printf("Demo data loaded\\n");')
    print('    return 0;')
    print('}')

if __name__ == "__main__":
    main()
