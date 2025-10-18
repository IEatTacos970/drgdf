def grab_research():
    with open('research_values.txt') as file:
        lines = [line.replace("[", "").replace("]", "").replace("'", "").replace(" ", "").rstrip() for line in file]
    ar_costs = []
    all_research = {
        "cn_costs": lines[0].split(','),#Comfortable Nests
        "ns_costs": lines[1].split(','),#Nutritional supplement
        "bi_costs": lines[2].split(','),#Better incubators
        "ec_costs": lines[3].split(','),#Excitable chickens
        "hhr_costs": lines[4].split(','),#Hen house remodel
        "ih_costs": lines[5].split(','),#Internal hatcheries
        "pp_costs": lines[6].split(','),#Padded  packaging
        "he_costs": lines[7].split(','),#Hatchery Expansion
        "be_costs": lines[8].split(','),#Bigger eggs
        "ihu_costs": lines[9].split(','),#Internal hatcher upgrades
        "il_costs": lines[10].split(','),#Improved leafsprings
        "vr_costs": lines[11].split(','),#Vehicle reliability
        "rb_costs": lines[12].split(','),#Rooster Booster"
        "cc_costs": lines[13].split(','),#Coordinated clucking
        "hr_costs": lines[14].split(','),#Hatchery rebuild
        "upc_costs": lines[15].split(','),#USDE prime certification
        "hha_costs": lines[16].split(','),#Hen house a/c
        "sfd_costs": lines[17].split(','),#Super feed diet
        "mcs_costs": lines[18].split(','),#Microlux chicken suites
        "ci_costs": lines[19].split(','),#Compact incubators
        "lb_costs": lines[20].split(','),#Lightweight boxes
        "dwe_costs": lines[21].split(','),#Depot worker exoskeletons
        "ihe_costs": lines[22].split(','),#Internal hatchery expansion
        "ig_costs": lines[23].split(','),#Improved genetics
        "tm_costs": lines[24].split(','),#Traffic management
        "mc_costs": lines[25].split(','),#Motivational clucking
        "dt_costs": lines[26].split(','),#Driver training
        "sf_costs": lines[27].split(','),#Shell fortification
        "elb_costs": lines[28].split(','),#Egg loading bots
        "saf_costs": lines[29].split(','),#Super alloy frames
        "ebe_costs": lines[30].split(','),#Even bigger eggs
        "ihe2_costs": lines[31].split(','),#Internal hatchery expansion 2
        "qes_cost": lines[32].split(','),#Quantum egg storage
        "gp_costs": lines[33].split(','),#Genetic purification
        "mli_costs": lines[34].split(','),#Machine learning incubators
        "tc_costs": lines[35].split(','),#Time compression
        "hu_costs": lines[36].split(','),  # Hover upgrades
        "gc_costs": lines[37].split(','),  # Graviton coating
        "gpl_costs": lines[38].split(','),  # Grav plating
        "cs_costs": lines[39].split(','),  # Crystalline shelling
        "av_costs": lines[40].split(','),  # Autonomous vehicles
        "nl_costs": lines[41].split(','),  # Neural linking
        "tw_costs": lines[42].split(','),  # Telepathic will
        "ech_costs": lines[43].split(','),  # Enlightened chickens
        "dc_costs": lines[44].split(','),  # Dark Containment
        "ap_costs": lines[45].split(','),  # Atomic purification
        "mul_costs": lines[46].split(','),  # Multiversal layering
        "td_costs": lines[47].split(','),  # Timeline diversion
        "wd_costs": lines[48].split(','),  # Wormhole dampening
        "em_costs": lines[49].split(','),  # Eggsistor miniaturization
        "gco_costs": lines[50].split(','),  # Graviton coupling
        "nnr_costs": lines[51].split(','),  # Neural net refinement
        "mr_costs": lines[52].split(','),  # Matter reconfiguration
        "ts_costs": lines[53].split(','),  # Timeline splicing
        "hp_costs": lines[54].split(','),  # Hyper portalling
        "ro_costs": lines[55].split(','),  # Relativity optimization
    }
    for list_items,current_list in all_research.items():
        temp_list = []
        for element in current_list:
            element = float(element)
            temp_list.append(element)
        current_list = temp_list
    temp_list = []
    research_req = [30,50,80,120,120,120,130,150,180,205,205,265]
    tier = 1
    rs_list = all_research.copy()
    dl_list = []
    while tier < 14:
        if tier > 1 and tier < 6:
            research = 5
            for list_items,current_list in rs_list.items():
                if research != 0:
                    temp_list.extend(current_list)
                    dl_list.append(list_items)
                    research -= 1
                else:
                    break
        else:
            research = 4
            for list_items,current_list in rs_list.items():
                if research != 0:
                    temp_list.extend(current_list)
                    dl_list.append(list_items)
                    research -= 1
                else:
                    break
        for x in dl_list:
            del rs_list[x]
        dl_list = []
        temp_list = list(map(float,temp_list))
        temp_list.sort()
        if tier == 13:
            ar_costs.extend(temp_list)
        else:
            ar_costs.extend(temp_list[:research_req[0]])
            del temp_list[:research_req[0]]
            research_req.pop(0)
        tier += 1
    return ar_costs,all_research

#30,80,160, 280, 400, 520, 650, 800, 980, 1185, 1390, 1655