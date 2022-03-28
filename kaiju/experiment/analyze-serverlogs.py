from os import listdir
from sys import argv
import matplotlib.pyplot as plt
import matplotlib

algos = ["LIST","LORA"]#,"BLOOM","STAMP"]
marks = {}
marks["LIST"] = "o"
marks["STAMP"] = "v"
marks["LORA"] = "x"
marks["BLOOM"] = "^"
names = {}
names["LIST"] = "RAMP-F"
names["STAMP"] = "RAMP-S"
names["BLOOM"] = "RAMP-H"
names["LORA"] = "LORA"

def plot_conc_clients_vs_throughput():
    d = argv[1]
    var = "Throughput"   
    final_results = {}
    ts = ["2250","2500","2750","3000"]
    for algo in algos:
        final_results[algo] = {}
    if var == "Throughput":
        var += "(ops/sec),"
    for f in listdir(argv[1]):
        if f.find("IT") == -1:
            continue
        #print f
        f = argv[1]+'/'+f
        results = {}
        for g in listdir(f):
            if g.find("C") == -1:
                continue
            g = f+'/'+g
            c = g.split("/C")[1]
            if results.get(c) is None:
                results[c] = 0
            lookout = False
            for line in open(g+"/run_out.log"):
                
                if line.find(var) != -1:
                    for word in line.split():
                        if word == var:
                            lookout = True
                        elif lookout:
                            results[c] += float(word)
                            lookout = False
        for algo in algos:
            if f.find(algo) != -1:
                for sz in ts:
                    if f.find(algo + "-4-THREADS" + sz) != -1:
                        if final_results[algo].get(sz) is None:
                            final_results[algo][sz] = 0
                        for c in results:
                            final_results[algo][sz] += results[c]
            


    x_axis = [2250,2500,2750,3000]
    fig = plt.figure(1)
    ax = plt.axes()
    plt.ylabel("Throughput (ops/s)")
    plt.xlabel("number of threads")
    mkfunc = lambda x, pos: '%1.1fM' % (x * 1e-6) if x >= 1e6 else '%1.1fK' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
    ax.yaxis.set_major_formatter(mkformatter)
    for algo in algos:
        y_axis = []
        for sz in ts:
            y_axis.append(float(final_results[algo][sz])/3)
        ax.plot(x_axis,y_axis, marker = marks[algo], label = names[algo])
        ax.legend()

    plt.show()
def plot_conc_clients_vs_latency():
    d = argv[1]
    var = "AverageLatency"    
    final_results = {}
    ts = ["2250","2500","2750","3000"]
    for algo in algos:
        final_results[algo] = {}
    if var == "AverageLatency":
        var += "(us),"
    for f in listdir(argv[1]):
        if f.find("IT") == -1:
            continue
        #print f
        f = argv[1]+'/'+f
        results = {}
        for g in listdir(f):
            if g.find("C") == -1:
                continue
            g = f+'/'+g
            c = g.split("/C")[1]
            if results.get(c) is None:
                results[c] = 0
            lookout = False
            opr = 0
            opw = 0
            latr = 0
            latw = 0
            for line in open(g+"/run_out.log"):
                if line.find("Operations,") != -1:
                    for word in line.split():
                        if word == "Operations,":
                            lookout = True
                        elif lookout:
                            lookout = False
                            if line.find("[UPDATE-TXN]") != -1:
                                opw = float(word)
                            else:
                                opr = float(word)
                
                if line.find(var) != -1:
                    for word in line.split():
                        if word == var:
                            lookout = True
                        elif lookout:
                            lookout = False
                            if line.find("[UPDATE-TXN]") != -1:
                                latw = float(word)
                            else:
                                latr = float(word)
            results[c] += (opr*latr*pow(10,-3) + opw+latw*pow(10,-3))/(opr+opw)
        for algo in algos:
            if f.find(algo) != -1:
                for sz in ts:
                    if f.find(algo + "-4-THREADS" + sz) != -1:
                        if final_results[algo].get(sz) is None:
                            final_results[algo][sz] = 0
                        for c in results:
                            final_results[algo][sz] += results[c]
            


    x_axis = [2250,2500,2750,3000]
    fig = plt.figure(2)
    ax = plt.axes()
    ax.set_yscale('log',base = 10)
    plt.ylabel("Average Latency (ms)")
    plt.xlabel("number of threads")
    for algo in algos:
        y_axis = []
        for sz in ts:
            y_axis.append(float(final_results[algo][sz])/3)
        ax.plot(x_axis,y_axis, marker = marks[algo], label = names[algo])
        ax.legend()
def plot_txnlen_vs_throughput():
    d = argv[1]
    var = "Throughput"
    final_results = {}
    ts = ["2","8","16","32","64","128"]

    for algo in algos:
        final_results[algo] = {}
    if var == "Throughput":
        var += "(ops/sec),"
    for f in listdir(argv[1]):
        if f.find("IT") == -1:
            continue
        #print f
        f = argv[1]+'/'+f
        results = {}
        for g in listdir(f):
            if g.find("C") == -1:
                continue
            g = f+'/'+g
            c = g.split("/C")[1]
            if results.get(c) is None:
                results[c] = 0
            lookout = False
            for line in open(g+"/run_out.log"):
                
                if line.find(var) != -1:
                    for word in line.split():
                        if word == var:
                            lookout = True
                        elif lookout:
                            results[c] += float(word)
                            lookout = False
        for algo in algos:
            if f.find(algo) != -1:
                for sz in ts:
                    if f.find(algo + "-" + sz) != -1:
                        if final_results[algo].get(sz) is None:
                            final_results[algo][sz] = 0
                        for c in results:
                            final_results[algo][sz] += results[c]
            


    x_axis = [2,8,16,32,64,128]
    fig = plt.figure(5)
    ax = plt.axes()
    plt.ylabel("Throughput (ops/s)")
    plt.xlabel("txn size (ops)")
    ax.set_xscale('log',base = 2)
    mkfunc = lambda x, pos: '%1.1fM' % (x * 1e-6) if x >= 1e6 else '%1.1fK' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
    ax.yaxis.set_major_formatter(mkformatter)
    for algo in algos:
        y_axis = []
        for sz in ts:
            y_axis.append(float(final_results[algo][sz])/3)
        ax.plot(x_axis,y_axis, marker = marks[algo], label = names[algo])
        ax.legend()

    plt.show()

def plot_lora_tp():
    d = argv[1]
    var = "Throughput"
    final_results = {}
    kls = ["1000","10000", "1000000"]
    rprops = ["0.5","0.75","0.95"]
    tlens = ["4","8","16","64","128"]
    la = len(tlens)
    lb = len(rprops)
    for algo in algos:
        final_results[algo] = {}
        for prop in rprops:
            final_results[algo][prop] = {}
            for tlen in tlens:
                final_results[algo][prop][tlen] = {}
                for l in kls:
                    final_results[algo][prop][tlen][l] = 0

    if var == "Throughput":
        var += "(ops/sec),"
    for f in listdir(argv[1]):
        if f.find("IT0") == -1:
            continue
        f = argv[1]+'/'+f
        a = ""
        kl = ""
        rprop = ""
        tlen = ""
        for algo in algos:
            if f.find("READ_ATOMIC_" + algo) != -1:
                a = algo
                break

        for prop in rprops:
            if f.find("RPROP" + prop + "-") != -1:
                rprop = prop
                break

        for l in tlens:
            if f.find(a + "-" + l) != -1:
                tlen = l
                break
        
        for l in kls:
            if f.find("NK" + l + "-") != -1:
                kl = l
                break
        results = {}
        for g in listdir(f):
            if g.find("C") == -1:
                continue
            g = f+'/'+g
            c = g.split("/C")[1]
            if results.get(c) is None:
                results[c] = 0
            lookout = False
            for line in open(g+"/run_out.log"):
                
                if line.find(var) != -1:
                    for word in line.split():
                        if word == var:
                            lookout = True
                        elif lookout:
                            results[c] += float(word)
                            lookout = False

        for c in results:
            final_results[a][rprop][tlen][kl] += results[c]

    x_axis = [1000, 10000, 1000000]
    [fig, axs] = plt.subplots(la,lb)
    plt.ylabel("Throughput (ops/s)")
    plt.xlabel("Num keys")
    
    mkfunc = lambda x, pos: '%1.1fM' % (x * 1e-6) if x >= 1e6 else '%1.1fK' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
    for i in range(0,la):
        for j in range(0,lb):
            axs[i,j].yaxis.set_major_formatter(mkformatter)
            axs[i,j].set_xscale('log',base = 10)
    i = 0
    for tlen in tlens:
        j = 0
        for rprop in rprops:
            for algo in algos:
                y_axis = []
                for kl in kls:
                    y_axis.append(float(final_results[algo][rprop][tlen][kl]))
                axs[i,j].plot(x_axis,y_axis, marker = marks[algo],label = names[algo])
                axs[i,j].set_title("tp vs num_keys at rprop = " + rprop + " and txn_len = " + tlen,{'fontsize' : 5})
            j += 1
        i += 1
    for ax in axs.flat:
        ax.label_outer()
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center')
    #fig.tight_layout()
    plt.show()

def plot_lora_lat():
    d = argv[1]
    var = "AverageLatency"    

    if var == "AverageLatency":
        var += "(us),"
    final_results = {}
    fr_read = {}
    fr_write = {}
    kls = ["1000","10000", "1000000"]
    rprops = ["0.5","0.75","0.95"]
    tlens = ["4","8","16","64","128"]
    la = len(tlens)
    lb = len(rprops)
    for algo in algos:
        final_results[algo] = {}
        fr_read[algo] = {}
        fr_write[algo] = {}
        for prop in rprops:
            final_results[algo][prop] = {}
            fr_read[algo][prop] = {}
            fr_write[algo][prop] = {}
            for tlen in tlens:
                final_results[algo][prop][tlen] = {}
                fr_read[algo][prop][tlen] = {}
                fr_write[algo][prop][tlen] = {}
                for l in kls:
                    final_results[algo][prop][tlen][l] = 0
                    fr_read[algo][prop][tlen][l] = 0
                    fr_write[algo][prop][tlen][l] = 0

    for f in listdir(argv[1]):
        if f.find("IT0") == -1:
            continue
        f = argv[1]+'/'+f
        a = ""
        kl = ""
        rprop = ""
        tlen = ""
        for algo in algos:
            if f.find("READ_ATOMIC_" + algo) != -1:
                a = algo
                break

        for prop in rprops:
            if f.find("RPROP" + prop + "-") != -1:
                rprop = prop
                break

        for l in tlens:
            if f.find(a + "-" + l + "-") != -1:
                tlen = l
                break
        if tlen == "":
            continue
        for l in kls:
            if f.find("NK" + l + "-") != -1:
                kl = l
                break
        results = {}
        rr = {}
        rw = {}
        for g in listdir(f):
            if g.find("C") == -1:
                continue
            g = f+'/'+g
            c = g.split("/C")[1]
            if results.get(c) is None:
                results[c] = 0
                rr[c] = 0
                rw[c] = 0
            lookout = False
            opr = 0
            opw = 0
            latr = 0
            latw = 0
            for line in open(g+"/run_out.log"):
                if line.find("Operations,") != -1:
                    for word in line.split():
                        if word == "Operations,":
                            lookout = True
                        elif lookout:
                            lookout = False
                            if line.find("[UPDATE-TXN]") != -1:
                                opw = float(word)
                            else:
                                opr = float(word)
                if line.find(var) != -1:
                    for word in line.split():
                        if word == var:
                            lookout = True
                        elif lookout:
                            lookout = False
                            if line.find("[UPDATE-TXN]") != -1:
                                latw = float(word)
                            else:
                                latr = float(word)
            if opr + opw == 0:
                results[c] += 0
                rr[c] += 0
                rw[c] += 0
            else:
                results[c] += (opr*latr*pow(10,-3) + opw+latw*pow(10,-3))/(opr+opw)
                rr[c] += latr*pow(10,-3)
                rw[c] += latw*pow(10,-3)
        for c in results:
            final_results[a][rprop][tlen][kl] += results[c]
            fr_read[a][rprop][tlen][kl] += rr[c]
            fr_write[a][rprop][tlen][kl] += rw[c]

    x_axis = [1000, 10000, 1000000]
    [fig, axs] = plt.subplots(la,lb)

    plt.ylabel("Average Latency (ms)")
    plt.xlabel("number of keys")
    plt.title("Avg Lat vs Num keys")
    for i in range(0,la):
        for j in range(0,lb):
            axs[i,j].set_yscale('log',base = 10)
            axs[i,j].set_xscale('log',base = 10)
    i = 0
    for tlen in tlens:
        j = 0
        for rprop in rprops:
            if rprop == "0":
                continue
            for algo in algos:
                y_axis = []
                for kl in kls:
                    y_axis.append(float(final_results[algo][rprop][tlen][kl])/5)
                axs[i,j].plot(x_axis,y_axis, marker = marks[algo],label = names[algo])
                axs[i,j].set_title("lat(ms) vs num_keys at rprop = " + rprop + " and txn_len = " + tlen,{'fontsize' : 5})
            j += 1
        i += 1
    for ax in axs.flat:
        ax.label_outer()
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center')
    #fig.tight_layout()
    plt.show()
    [fig, axs] = plt.subplots(la,lb)

    plt.ylabel("Average Latency (ms)")
    plt.xlabel("number of keys")
    plt.title("Avg Read Lat vs Num keys")
    for i in range(0,la):
        for j in range(0,lb):
            axs[i,j].set_yscale('log',base = 10)
            axs[i,j].set_xscale('log',base = 10)
    i = 0
    for tlen in tlens:
        j = 0
        for rprop in rprops:
            if rprop == "0":
                continue
            for algo in algos:
                y_axis = []
                for kl in kls:
                    y_axis.append(float(fr_read[algo][rprop][tlen][kl])/5)
                axs[i,j].plot(x_axis,y_axis, marker = marks[algo],label = names[algo])
                axs[i,j].set_title("lat(ms) vs num_keys at rprop = " + rprop + " and txn_len = " + tlen,{'fontsize' : 5})
            j += 1
        i += 1
    for ax in axs.flat:
        ax.label_outer()
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center')
    #fig.tight_layout()
    plt.show()
    [fig, axs] = plt.subplots(la,lb)

    plt.ylabel("Average Latency (ms)")
    plt.xlabel("number of keys")
    plt.title("Avg Write Lat vs Num keys")
    for i in range(0,la):
        for j in range(0,lb):
            axs[i,j].set_yscale('log',base = 10)
            axs[i,j].set_xscale('log',base = 10)
    i = 0
    for tlen in tlens:
        j = 0
        for rprop in rprops:
            if rprop == "0":
                continue
            for algo in algos:
                y_axis = []
                for kl in kls:
                    y_axis.append(float(fr_write[algo][rprop][tlen][kl])/5)
                axs[i,j].plot(x_axis,y_axis, marker = marks[algo],label = names[algo])
                axs[i,j].set_title("lat(ms) vs num_keys at rprop = " + rprop + " and txn_len = " + tlen,{'fontsize' : 5})
            j += 1
        i += 1
    for ax in axs.flat:
        ax.label_outer()
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, loc='upper center')
    #fig.tight_layout()
    plt.show()

def plot_perc_reads_vs_throughput():
    d = argv[1]
    var = "Throughput"
    final_results = {}
    ts = ["1", "0.75", "0.5","0.25", "0"]
    for algo in algos:
        final_results[algo] = {}
    if var == "Throughput":
        var += "(ops/sec),"
    for f in listdir(argv[1]):
        if f.find("IT") == -1:
            continue
        #print f
        f = argv[1]+'/'+f
        results = {}
        for g in listdir(f):
            if g.find("C") == -1:
                continue
            g = f+'/'+g
            c = g.split("/C")[1]
            if results.get(c) is None:
                results[c] = 0
            lookout = False
            for line in open(g+"/run_out.log"):
                
                if line.find(var) != -1:
                    for word in line.split():
                        if word == var:
                            lookout = True
                        elif lookout:
                            results[c] += float(word)
                            lookout = False
        for algo in algos:
            if f.find(algo) != -1:
                for sz in ts:
                    if f.find(algo + "-4-THREADS1000-RPROP" + sz + "-") != -1:
                        if final_results[algo].get(sz) is None:
                            final_results[algo][sz] = 0
                        for c in results:
                            final_results[algo][sz] += results[c]
            


    x_axis = [1, 0.75, 0.5, 0.25, 0]
    fig = plt.figure(4)
    ax = plt.axes()
    plt.ylabel("Throughput (ops/s)")
    plt.xlabel("read proportion")
    mkfunc = lambda x, pos: '%1.1fM' % (x * 1e-6) if x >= 1e6 else '%1.1fK' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
    ax.yaxis.set_major_formatter(mkformatter)
    for algo in algos:
        y_axis = []
        for sz in ts:
            y_axis.append(float(final_results[algo][sz])/3)
        ax.plot(x_axis,y_axis, marker = marks[algo], label = names[algo])
        ax.legend()

    plt.show()

def plot_numkeys_vs_throughput():
    d = argv[1]
    var = "Throughput"
    final_results = {}
    ts = ["10", "100", "1000","10000", "100000","10000000"]
    for algo in algos:
        final_results[algo] = {}
    if var == "Throughput":
        var += "(ops/sec),"
    for f in listdir(argv[1]):
        if f.find("IT") == -1:
            continue
        f = argv[1]+'/'+f
        results = {}
        for g in listdir(f):
            if g.find("C") == -1:
                continue
            g = f+'/'+g
            c = g.split("/C")[1]
            if results.get(c) is None:
                results[c] = 0
            lookout = False
            for line in open(g+"/run_out.log"):
                
                if line.find(var) != -1:
                    for word in line.split():
                        if word == var:
                            lookout = True
                        elif lookout:
                            results[c] += float(word)
                            lookout = False
        for algo in algos:
            if f.find("READ_ATOMIC_" + algo) != -1:
                for sz in ts:
                    if f.find("-4-THREADS1000-RPROP0.95-VS1-TXN4-NC5-NS5-NK" + sz + "-DCP0.000000-CCD-1-IT") != -1:
                        if final_results[algo].get(sz) is None:
                            final_results[algo][sz] = 0
                        for c in results:
                            final_results[algo][sz] += results[c]

    x_axis = [10, 100, 1000, 10000]
    fig = plt.figure(7)
    ax = plt.axes()
    plt.ylabel("Throughput (ops/s)")
    plt.xlabel("Num keys")
    
    mkfunc = lambda x, pos: '%1.1fM' % (x * 1e-6) if x >= 1e6 else '%1.1fK' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
    ax.yaxis.set_major_formatter(mkformatter)
    for algo in algos:
        y_axis = []
        for sz in ts:
            if sz == "10000000" or sz == "100000":
                continue
            y_axis.append(float(final_results[algo][sz])/3)
        ax.plot(x_axis,y_axis, marker = marks[algo], label = names[algo])
        ax.legend()
    plt.show()

def plot_value_size_vs_throughput():
    d = argv[1]
    var = "Throughput"
    final_results = {}
    ts = ["10", "100", "1000","10000", "100000","10000000"]
    for algo in algos:
        final_results[algo] = {}
    if var == "Throughput":
        var += "(ops/sec),"
    for f in listdir(argv[1]):
        if f.find("IT") == -1:
            continue
        #print f
        f = argv[1]+'/'+f
        results = {}
        for g in listdir(f):
            if g.find("C") == -1:
                continue
            g = f+'/'+g
            c = g.split("/C")[1]
            if results.get(c) is None:
                results[c] = 0
            lookout = False
            for line in open(g+"/run_out.log"):
                
                if line.find(var) != -1:
                    for word in line.split():
                        if word == var:
                            lookout = True
                        elif lookout:
                            results[c] += float(word)
                            lookout = False
        for algo in algos:
            if f.find(algo) != -1:
                for sz in ts:
                    if f.find(algo + "-4-THREADS1000-RPROP0.95-VS" + sz + "-") != -1:
                        if final_results[algo].get(sz) is None:
                            final_results[algo][sz] = 0
                        for c in results:
                            final_results[algo][sz] += results[c]
            


    x_axis = [10, 100, 1000, 10000, 100000, 10000000]
    fig = plt.figure(3)
    ax = plt.axes()
    plt.ylabel("Throughput (ops/s)")
    plt.xlabel("Value size (bytes)")
    
    mkfunc = lambda x, pos: '%1.1fM' % (x * 1e-6) if x >= 1e6 else '%1.1fK' % (x * 1e-3) if x >= 1e3 else '%1.1f' % x
    mkformatter = matplotlib.ticker.FuncFormatter(mkfunc)
    ax.yaxis.set_major_formatter(mkformatter)
    for algo in algos:
        y_axis = []
        for sz in ts:
            y_axis.append(float(final_results[algo][sz])/3)
        ax.plot(x_axis,y_axis, marker = marks[algo], label = names[algo])
        ax.legend()

    plt.show()    



accepted_args = ["txnlen","threads","rprop","valuesize","numkeys","lora"]

if __name__ == "__main__":
    if argv[2] == "txnlen":
        plot_txnlen_vs_throughput()
    elif argv[2] == "threads":
        plot_conc_clients_vs_latency()
        plot_conc_clients_vs_throughput()
    elif argv[2] == "rprop":
        plot_perc_reads_vs_throughput()
    elif argv[2] == "valuesize":
        plot_value_size_vs_throughput()
    elif argv[2] == "numkeys":
        plot_numkeys_vs_throughput()
    elif argv[2] == "lora":
        plot_lora_tp()
        plot_lora_lat()
    else:
        print("Could not recognize arg: " + argv[2])
        print("Usage: python analyze_logs.py /path/to/dir argv[2] where argv[2] one of:")
        print(accepted_args)


