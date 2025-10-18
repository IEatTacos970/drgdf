import math
import copy

from research_values import grab_research

a_multi = float(input("Artifact Multiplier: "))
cube = float(input("Research discount (T4C = 50): "))
mx_off = int(input("Max offline (in seconds) for 1 research (3600 recommended): "))
mxh_off = int(input("Max offline (in seconds) for 1 hab/vehicle (86400 recommended): "))
c_multi = 6
te_multii = int(input("# of TE: "))
te_multi = 1.1**te_multii

class Farm:
    def __init__(self,multi,elr,ship,upgrades):
        self.elr = elr
        self.ship = ship
        self.multi = multi
        self.upgrades = upgrades
        self.ihr = 0
        self.cr = 205
        self.cash = 0
        self.house = [1,0,0,0]
        self.pop = 250
        self.vehicles = [1,0,0,0]
        self.vehicle_count = 4
        self.shipping = [5000,0,0,0]
        self.car_max = 4
        self.cars = 0
    def updateELR(self,x,y):
        self.elr[x] += y
    def updateShip(self,x,y):
        self.ship[x] += y
    def updateMulti(self,x,y):
        self.multi[x] += y
    def updateUpgrades(self,x,y):
        self.upgrades[x] += y
    def updateIHR(self,x):
        self.ihr += x
    def updateCR(self,x):
        self.cr += x
    def printTier(self,file):
        t = 1
        temp = []
        while t < 14:
            if t > 1 and t < 6:
                file.write("Tier "+str(t)+": "+str(self.upgrades[:5])+'\n')
                temp.extend(self.upgrades[:5])
                del self.upgrades[:5]
            else:
                file.write("Tier " + str(t) + ": " + str(self.upgrades[:4])+'\n')
                temp.extend(self.upgrades[:4])
                del self.upgrades[:4]
            t+=1
        self.upgrades = temp
        file.write("Houses: "+str(self.house)+'\n')
        file.write("Vehicles: " + str(self.vehicles)+'\n')
        file.write("Cars: "+str(self.cars)+'\n\n')
    def popInit(self):
        x = 0
        while x < 4:
            self.house[x] = 2
            x+=1
        self.pop = 2000
    def popUpdate(self):
        reg = min(self.house)
        ind = self.house.index(reg)
        self.house[ind] += 1
        match reg:
            case 2: farm.pop += 500
            case 3: farm.pop += 1000
            case 4: farm.pop += 3000
            case 5: farm.pop += 5000
            case 6: farm.pop += 10000
            case 7: farm.pop += 30000
            case 8: farm.pop += 50000
            case 9: farm.pop += 100000
            case 10: farm.pop += 300000
            case 11: farm.pop += 500000
            case 12: farm.pop += 1000000
            case 13: farm.pop += 3000000
            case 14: farm.pop += 5000000
            case 15: farm.pop += 15000000
            case 16: farm.pop += 25000000
            case 17: farm.pop += 50000000
            case 18: farm.pop += 500000000
    def incrVehicle(self):
        self.vehicle_count += 1
    def incrCars(self):
        self.car_max += 1
    def vehicleInit(self):
        add_amount = self.vehicle_count - len(self.vehicles)
        x = 0
        while add_amount > x:
            self.vehicles.append(0)
            self.shipping.append(0)
            x += 1
    def vehicleUpdate(self,x,shipping):
        reg = min(self.vehicles)
        if reg >= x:
            return
        elif x != 13:
            ind = self.vehicles.index(reg)
            self.vehicles[ind] = x
            self.shipping[ind] = shipping
        else:
            if self.cars < self.car_max:
                self.cars += 1
    def trueShip(self):
        ship = 0
        for x in self.shipping:
            ship += x
        hyperloop = self.vehicles.count(12)
        ship += hyperloop*self.cars*50000000
        return ship * 2.5/60 * 1.1025

offline = 180
base_elr = 4/60 * 1.05

ar_costs,all_research = grab_research()
farm = Farm([te_multi,c_multi,a_multi,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[base_elr,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])
vehicles = {
    "Trike": [0.00, 278.00, 462.00, 684.00, 952.00, 1270.00, 1650.00, 2094.00, 2616.00, 3218.00, 3916.00, 4720.00, 5634.00, 6680.00, 7864.00, 9198.00, 10706.00],
    "TV": [2888.00, 3458.00, 4096.00, 4800.00, 5582.00, 6454.00, 7412.00, 8460.00, 9618.00, 10890.00, 12278.00, 13784.00, 15434.00, 17234.00, 19180.00, 21278.00, 23560.00],
    "Pickup": [10574.00, 13946.00, 18048.00, 22988.00, 28876.00, 35862.00, 44074.00, 53670.00, 64842.00, 77700.00, 92566.00, 109476.00, 128830.00, 150784.00, 175480.00, 203456.00, 234764.00],
    "10ft": [78334.00, 137348.00, 226684.00, 356812.00, 540378.00, 792350.00, 1130316.00, 1574154.00, 2146524.00, 2873784.00, 3787892.00, 4918364.00, 6301486.00, 7985104.00, 10001614.00, 12413864.00, 15261010.00],
    "24ft": [1415714.00, 3167982.00, 6331184.00, 11629436.00, 19971308.00, 32529500.00, 50720980.00, 76237064.00, 111078260.00, 157574560.00, 218422000.00, 296782000.00, 396108000.00, 520068000.00, 673188000.00, 860754000.00, 1087032000.00],
    "Semi": [38872660.00, 69858882.00, 118059160.00, 189661200.00, 292240000.00, 434910000.00, 628390000.00, 885046000.00, 1218930000.00, 1645960000.00, 2184000000.00, 2856000000.00, 3682000000.00, 4686000000.00, 5902000000.00, 7352000000.00, 9076000000.00],
    "Double": [825560000.00, 1945412000.00, 4036000000.00, 7616000000.00, 13368000000.00, 22134000000.00, 34976000000.00, 53148000000.00, 78136000000.00, 111678000000.00, 155772000000.00, 212716000000.00, 285198000000.00, 376050000000.00, 488352000000.00, 625964000000.00, 793004000000.00],
    "Future": [380014000000000.00, 8126000000000000.00, 52218000000000000.00, 199416000000000000.00, 568500000000000000.00, 1343078000000000000.00, 2786000000000000000.00, 5250000000000000000.00, 9186000000000000000.00, 15172000000000000000.00, 23892000000000000000.00, 36172000000000000000.00, 52992000000000000000.00, 75492000000000000000.00, 104978000000000000000.00, 142908000000000000000.00, 190924000000000000000.00],
    "Mega": [3170000000000000000.00, 11222000000000000000.00, 30506000000000000000.00, 69806000000000000000.00, 141404000000000000000.00, 261588000000000000000.00, 451482000000000000000.00, 736576000000000000000.00, 1148912000000000000000.00, 1725842000000000000000.00, 2512000000000000000000.00, 3556000000000000000000.00, 4916000000000000000000.00, 6650000000000000000000.00, 8828000000000000000000.00, 11520000000000000000000.00, 14810000000000000000000.00],
    "Hover": [1349836000000000000000.00, 6218000000000000000000.00, 19488000000000000000000.00, 48648000000000000000000.00, 104462000000000000000000.00, 201444000000000000000000.00, 358270000000000000000000.00, 598600000000000000000000.00, 950606000000000000000000.00, 1447940000000000000000000.00, 2130000000000000000000000.00, 3044000000000000000000000.00, 4244000000000000000000000.00, 5786000000000000000000000.00, 7740000000000000000000000.00, 10176000000000000000000000.00, 13178000000000000000000000.00],
    "Quantum": [310576000000000000000000.00, 751332000000000000000000.00, 1580394000000000000000000.00, 3002000000000000000000000.00, 5282000000000000000000000.00, 8742000000000000000000000.00, 13782000000000000000000000.00, 20874000000000000000000000.00, 30564000000000000000000000.00, 43488000000000000000000000.00, 60368000000000000000000000.00, 82022000000000000000000000.00, 109388000000000000000000000.00, 143514000000000000000000000.00, 185448000000000000000000000.00, 236450000000000000000000000.00, 298054000000000000000000000.00],
    "Hyper": [825914000000000000000000000.00, 8910000000000000000000000000.00, 42922000000000000000000000000.00, 139118000000000000000000000000.00, 356106000000000000000000000000.00, 779208000000000000000000000000.00, 1524150000000000000000000000000.00, 2740000000000000000000000000000.00, 4620000000000000000000000000000.00, 7388000000000000000000000000000.00, 11322000000000000000000000000000.00, 16746000000000000000000000000000.00, 24032000000000000000000000000000.00, 33612000000000000000000000000000.00, 45976000000000000000000000000000.00, 61680000000000000000000000000000.00, 81310000000000000000000000000000.00],
    "Cars": [101908000000000000000000000.00, 617834000000000000000000000.00, 2266000000000000000000000000.00, 6264000000000000000000000000.00, 14450000000000000000000000000.00, 29372000000000000000000000000.00, 54380000000000000000000000000.00, 93780000000000000000000000000.00, 152738000000000000000000000000.00]
}

def calc_cash():
    cash_multi = math.prod(farm.multi)
    elr_multi = math.prod(farm.elr) * farm.pop
    ship_multi = math.prod(farm.ship) * farm.trueShip()
    return cash_multi * min(elr_multi, ship_multi) * 1.05 * 2

def research_sim():
    seconds = 0
    while mx_off>seconds:
        farm.cash += calc_cash()
        while farm.cash > ar_costs[0] * 1/cube:
            farm.cash -= ar_costs[0] * 1/cube
            re_list = ""
            for list_name, current_list in all_research.items():
                for element in current_list:
                    if float(element) == float(ar_costs[0]):
                        re_list = list_name
                        current_list.pop(0)
                        break
                else:
                    continue
                break
            match re_list:
                case "cn_costs": farm.updateELR(2,0.1),farm.updateUpgrades(0,1)
                case "ns_costs": farm.updateMulti(3,0.25),farm.updateUpgrades(1,1)
                case "bi_costs": farm.updateUpgrades(2,1)
                case "ec_costs": farm.updateUpgrades(3,1)
                case "hhr_costs": farm.updateELR(3,0.05),farm.updateUpgrades(4,1)
                case "ih_costs": farm.updateIHR(4),farm.updateUpgrades(5,1)
                case "pp_costs": farm.updateMulti(4,0.25),farm.updateUpgrades(6,1)
                case "he_costs": farm.updateUpgrades(7,1)
                case "be_costs": farm.updateMulti(5,farm.multi[5]),farm.updateUpgrades(8,1)
                case "ihu_costs": farm.updateIHR(10),farm.updateUpgrades(9,1)
                case "il_costs": farm.updateShip(1,0.05),farm.updateUpgrades(10,1)
                case "vr_costs": farm.incrVehicle(),farm.updateUpgrades(11,1)
                case "rb_costs": farm.updateUpgrades(12,1)
                case "cc_costs": farm.updateCR(0.2),farm.updateUpgrades(13,1)
                case "hr_costs": farm.updateUpgrades(14,1)
                case "upc_costs": farm.updateMulti(6,farm.multi[6]*2),farm.updateUpgrades(15,1)
                case "hha_costs": farm.updateELR(4,0.05),farm.updateUpgrades(16,1)
                case "sfd_costs": farm.updateMulti(7,0.25),farm.updateUpgrades(17,1)
                case "mcs_costs": farm.updateELR(5,0.05),farm.updateUpgrades(18,1)
                case "ci_costs": farm.updateUpgrades(19,1)
                case "lb_costs": farm.updateShip(2,0.1),farm.updateUpgrades(20,1)
                case "dwe_costs": farm.incrVehicle(),farm.updateUpgrades(21,1)
                case "ihe_costs": farm.updateIHR(20),farm.updateUpgrades(22,1)
                case "ig_costs": farm.updateMulti(8,0.15),farm.updateELR(6,0.15),farm.updateUpgrades(23,1)
                case "tm_costs": farm.incrVehicle(),farm.updateUpgrades(24,1)
                case "mc_costs": farm.updateCR(0.5),farm.updateUpgrades(25,1)
                case "dt_costs": farm.updateShip(3,0.05),farm.updateUpgrades(26,1)
                case "sf_costs": farm.updateMulti(9,0.15),farm.updateUpgrades(27,1)
                case "elb_costs": farm.incrVehicle(),farm.updateUpgrades(28,1)
                case "saf_costs": farm.updateShip(4,0.05),farm.updateUpgrades(29,1)
                case "ebe_costs": farm.updateMulti(10,farm.multi[10]),farm.updateUpgrades(30,1)
                case "ihe2_costs": farm.updateIHR(50),farm.updateUpgrades(31,1)
                case "qes_cost": farm.updateShip(5,0.05),farm.updateUpgrades(32,1)
                case "gp_costs": farm.updateMulti(11,0.1),farm.updateUpgrades(33,1)
                case "mli_costs": farm.updateIHR(10),farm.updateUpgrades(34,1)
                case "tc_costs": farm.updateELR(7,0.1),farm.updateUpgrades(35,1)
                case "hu_costs": farm.updateShip(6,0.05),farm.updateUpgrades(36,1)
                case "gc_costs": farm.updateMulti(12,farm.multi[12]),farm.updateUpgrades(37,1)
                case "gpl_costs": farm.updateELR(8,0.02),farm.updateUpgrades(38,1)
                case "cs_costs": farm.updateMulti(13,0.25),farm.updateUpgrades(39,1)
                case "av_costs": farm.incrVehicle(),farm.updateUpgrades(40,1)
                case "nl_costs": farm.updateIHR(100),farm.updateUpgrades(41,1)
                case "tw_costs": farm.updateMulti(14,0.25),farm.updateUpgrades(42,1)
                case "ech_costs": farm.updateCR(2),farm.updateUpgrades(43,1)
                case "dc_costs": farm.updateShip(7,0.05),farm.updateUpgrades(44,1)
                case "ap_costs": farm.updateMulti(15,0.1),farm.updateUpgrades(45,1)
                case "mul_costs": farm.updateMulti(16,farm.multi[16]*9),farm.updateUpgrades(46,1)
                case "td_costs": farm.updateELR(9,0.02),farm.updateUpgrades(47,1)
                case "wd_costs": farm.updateELR(10,0.02),farm.updateUpgrades(48,1)
                case "em_costs": farm.updateMulti(17,0.05),farm.updateUpgrades(49,1)
                case "gco_costs": farm.incrCars(),farm.updateUpgrades(50,1)
                case "nnr_costs": farm.updateShip(8,0.05),farm.updateUpgrades(51,1)
                case "mr_costs": farm.updateMulti(18,0.01),farm.updateUpgrades(52,1)
                case "ts_costs": farm.updateMulti(19,farm.multi[19]*9),farm.updateUpgrades(53,1)
                case "hp_costs": farm.updateShip(9,0.05),farm.updateUpgrades(54,1)
                case "ro_costs": farm.updateELR(11,0.1),farm.updateUpgrades(55,1)
            ar_costs.pop(0)
            seconds = 0
        seconds += 1
    farm.cash = 0
def house_sim():
    house = [6.92, 197.00, 467.00, 816.00, 4134.00, 6649.00, 10016.00, 14425.00, 61076.00, 127276.00, 238583.00,
             415193.00,
             1377000.00, 2627000.00, 4637000.00, 7704000.00, 26944000.00, 54319000.00, 100061000.00, 172278000.00,
             951992000.00,
             2555000000.00, 5801000000.00, 11703000000.00, 51574000000.00, 109062000000.00, 208428000000.00,
             369239000000.00,
             1480000000000.00, 3143000000000.00, 6024000000000.00, 10692000000000.00, 63612000000000.00,
             175151000000000.00,
             404250000000000.00, 824484000000000.00, 3690000000000000.00, 7831000000000000.00, 14997000000000000.00,
             26576000000000000.00,
             106392000000000000.00, 225434000000000000.00, 431103000000000000.00, 763129000000000000.00,
             4496000000000000000.00,
             12304000000000000000.00, 28244000000000000000.00, 57332000000000000000.00, 297859000000000000000.00,
             701448000000000000000.00,
             1449000000000000000000.00, 2721000000000000000000.00, 21221000000000000000000.00,
             65697000000000000000000.00, 162707000000000000000000.00,
             347477000000000000000000.00, 4098000000000000000000000.00, 15190000000000000000000000.00,
             42223000000000000000000000.00, 97741000000000000000000000.00,
             2135000000000000000000000000.00, 10285000000000000000000000000.00, 33323000000000000000000000000.00,
             85225000000000000000000000000.00,
             19692000000000000000000000000000.00, 146005000000000000000000000000000.00,
             592272000000000000000000000000000.00, 1740000000000000000000000000000000.00]
    seconds = 0
    farm.popInit()
    while mxh_off > seconds:
        farm.cash += calc_cash()
        try:
            while farm.cash > house[0]:
                farm.cash -= house[0]
                farm.popUpdate()
                house.pop(0)
                seconds = 0
        except:
            return
        seconds += 1
    farm.cash = 0
    return
def vehicle_sim():
    local_vehicle = copy.deepcopy(vehicles)
    seconds = 0
    buy_list = []
    del local_vehicle["Cars"][farm.car_max:]
    for x in local_vehicle.values():
        del x[farm.vehicle_count:]
        buy_list.extend(x)
    buy_list.sort()
    buy_list.pop(0)
    farm.vehicleInit()
    ve_list = ""
    while mxh_off > seconds:
        farm.cash += calc_cash()
        try:
            while farm.cash > buy_list[0]:
                farm.cash -= buy_list[0]
                ve_num = 0
                shipping = 0
                for list_name, current_list in vehicles.items():
                    for element in current_list:
                        if float(element) == float(buy_list[0]):
                            ve_list = list_name
                            break
                    else:
                        continue
                    break
                match ve_list:
                    case "Trike": ve_num,shipping = 1,5000
                    case "TV": ve_num,shipping = 2,15000
                    case "Pickup": ve_num,shipping = 3,50000
                    case "10ft": ve_num,shipping = 4,100000
                    case "24ft": ve_num,shipping = 5,250000
                    case "Semi": ve_num,shipping = 6,500000
                    case "Double": ve_num,shipping = 7,1000000
                    case "Future": ve_num,shipping = 8,5000000
                    case "Mega": ve_num,shipping = 9,15000000
                    case "Hover": ve_num,shipping = 10,30000000
                    case "Quantum": ve_num,shipping = 11,50000000
                    case "Hyper": ve_num,shipping = 12,50000000
                    case "Cars": ve_num = 13
                farm.vehicleUpdate(ve_num,shipping)
                buy_list.pop(0)
                seconds = 0
        except:
            return
        seconds += 1
    farm.cash = 0
    return
def loop(f):
    research_sim()
    house_sim()
    vehicle_sim()
    cpm = calc_cash()
    cpm = int(cpm) * 60

    max_pop = farm.pop * farm.elr[3] * farm.elr[5] * farm.elr[8] * farm.elr[10]

    cash_multi = math.prod(farm.multi) / (farm.multi[1] * farm.multi[2])
    elr_multi = math.prod(farm.elr) * farm.pop * 3600
    ship_multi = math.prod(farm.ship) * farm.trueShip() * 3600
    eff_ship = min(elr_multi, ship_multi)

    Pe = max_pop * min(1, (ship_multi / elr_multi))

    f_value = 30000 * 2 * cash_multi * (elr_multi / max_pop) * (farm.cr - 4) ** 0.25 * 6 * (
                Pe + (0.2 * (max_pop - Pe)) + (farm.ihr * offline))
    d_value = f_value * 0.05

    def oom_calc(val):
        oom = round((len(f'{val:.0f}') - 2) / 3)
        eb = "uhhhh"
        match oom:
            case 1:
                eb = 'k'
            case 2:
                eb = 'm'
            case 3:
                eb = 'b'
            case 4:
                eb = 'T'
            case 5:
                eb = 'q'
            case 6:
                eb = 'Q'
            case 7:
                eb = 's'
            case 8:
                eb = 'S'
            case 9:
                eb = 'o'
            case 10:
                eb = 'n'
            case 11:
                eb = 'd'
            case 12:
                eb = 'U'
            case 13:
                eb = 'D'
            case 14:
                eb = 'Td'
            case 15:
                eb = 'qd'
            case 16:
                eb = 'Qd'
            case 17:
                eb = 'sd'
            case 18:
                eb = 'Sd'
        temp = round(val / 10 ** (oom * 3), 3)
        return str(temp) + eb

    d_value = oom_calc(d_value)
    cpm = oom_calc(cpm)
    eff_ship = oom_calc(eff_ship)
    elr_multi = oom_calc(elr_multi)
    ship_multi = oom_calc(ship_multi)
    f_value = oom_calc(f_value)

    f.write("Farm Value: " + f_value + " (Hopefully right?)"+'\n')
    f.write("Drone Value: " + d_value+'\n')
    f.write(cpm + " per minute"+'\n')
    f.write(eff_ship + " per hour"+'\n')
    f.write(elr_multi + " eggs per hour"+'\n')
    f.write(ship_multi + " ship per hour"+'\n')
    farm.printTier(f)

name = str(te_multii)+" - "+str(int(a_multi))+'.txt'
f = open(name, "w")
f.write("Artifact Multiplier: "+str(a_multi)+'\n')
f.write("Research discount (T4C = 50): "+str(cube)+'\n')
f.write("Max offline (in seconds) for 1 research: "+str(mx_off)+'\n')
f.write("Max offline (in seconds) for 1 hab/vehicle: "+str(mxh_off)+'\n')
f.write("Offline Colleggtible Multiplier: "+str(c_multi)+'\n')
f.write("# of TE: "+str(te_multii)+'\n\n')
loop(f)
loop(f)