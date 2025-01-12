# Reference:
# Li Z, Dutta S, Sheng J, Tran PN, Wu W, Chang K, Mdluli T, Strauss DG,
# Colatsky T. Improving the In Silico Assessment of Proarrhythmia Risk by
# Combining hERG (Human Ether-Ã -go-go-Related Gene) Channel-Drug Binding
# Kinetics and Multichannel Pharmacology. Circ Arrhythm Electrophysiol.
# 2017 Feb;10(2):e004628. doi: 10.1161/CIRCEP.116.004628.

import numpy as np

import modelling


class BindingParameters(object):
    """
    To create a library of all the dynamic hERG-binding parameters for
    different drug compounds.
    (ref. Table 2)
    """

    def __init__(self):
        super(BindingParameters, self).__init__()

        self.drug_compounds = ['dofetilide', 'bepridil', 'terfenadine',
                               'cisapride', 'verapamil', 'ranolazine',
                               'quinidine', 'sotalol', 'chlorpromazine',
                               'ondansetron', 'diltiazem', 'mexiletine',
                               'droperidol']
        self.binding_parameters = {
            'dofetilide': {
                'Kmax': 1e8,
                'Ku': 1.79e-5,
                'EC50': 5.483e8,
                'N': 0.9999,
                'Vhalf': -1.147,
                'Cmax': 2
            },
            'bepridil': {
                'Kmax': 3.735e7,
                'Ku': 1.765e-4,
                'EC50': 1e9,
                'N': 0.9365,
                'Vhalf': -54.93,
                'Cmax': 33
            },
            'terfenadine': {
                'Kmax': 9884,
                'Ku': 8.18e-5,
                'EC50': 41380,
                'N': 0.65,
                'Vhalf': -77.49,
                'Cmax': 4
            },
            'cisapride': {
                'Kmax': 9.997,
                'Ku': 4.161e-4,
                'EC50': 42.06,
                'N': 0.9728,
                'Vhalf': -199.5,
                'Cmax': 2.6
            },
            'cisapride_kmax_verapamil': {
                'Kmax': 4.646e4,
                'Ku': 4.161e-4,
                'EC50': 42.06,
                'N': 0.9728,
                'Vhalf': -199.5,
                'Cmax': 2.6
            },
            'cisapride_kmax_bepridil': {
                'Kmax': 3.735e7,
                'Ku': 4.161e-4,
                'EC50': 42.06,
                'N': 0.9728,
                'Vhalf': -199.5,
                'Cmax': 2.6
            },
            'cisapride_EC50_ranolazine': {
                'Kmax': 9.997,
                'Ku': 4.161e-4,
                'EC50': 1.472e5,
                'N': 0.9728,
                'Vhalf': -199.5,
                'Cmax': 2.6
            },
            'cisapride_EC50_verapamil': {
                'Kmax': 9.997,
                'Ku': 4.161e-4,
                'EC50': 9.184e6,
                'N': 0.9728,
                'Vhalf': -199.5,
                'Cmax': 2.6
            },
            'cisapride_kmax_EC50_verapamil': {
                'Kmax': 4.646e4,
                'Ku': 4.161e-4,
                'EC50': 9.184e6,
                'N': 0.9728,
                'Vhalf': -199.5,
                'Cmax': 2.6
            },
            'verapamil': {
                'Kmax': 4.646e4,
                'Ku': 7.927e-4,
                'EC50': 9.184e6,
                'N': 1.043,
                'Vhalf': -100,
                'Cmax': 81
            },
            'ranolazine': {
                'Kmax': 55.84,
                'Ku': 1.929e-2,
                'EC50': 1.472e5,
                'N': 0.95,
                'Vhalf': -94.87,
                'Cmax': 1948.2
            },
            'mexiletine': {
                'Kmax': 9.996,
                'Ku': 9.967e-2,
                'EC50': 2.308e6,
                'N': 1.304,
                'Vhalf': -86.26,
                'Cmax': 4129
            },
            'quinidine': {
                'Kmax': 5770,
                'Ku': 1e-2,
                'EC50': 1e6,
                'N': 0.8311,
                'Vhalf': -64.87,
                'Cmax': 3237
            },
            'sotalol': {
                'Kmax': 2403,
                'Ku': 1.985e-2,
                'EC50': 9.619e6,
                'N': 0.7516,
                'Vhalf': -55,
                'Cmax': 14690
            },
            'chlorpromazine': {
                'Kmax': 206000,
                'Ku': 3.866e-2,
                'EC50': 5.677e7,
                'N': 0.8871,
                'Vhalf': -14.57,
                'Cmax': 38
            },
            'ondansetron': {
                'Kmax': 33540,
                'Ku': 2.325e-2,
                'EC50': 9.95e6,
                'N': 0.8874,
                'Vhalf': -82.11,
                'Cmax': 139
            },
            'diltiazem': {
                'Kmax': 251,
                'Ku': 2.816e-1,
                'EC50': 1e6,
                'N': 0.9485,
                'Vhalf': -90.89,
                'Cmax': 122
            },
            'droperidol': {
                'Kmax': 14.21,
                'Ku': 1.256e-3,
                'EC50': 116.5,
                'N': 0.578,
                'Vhalf': -78.68,
                'Cmax': 6.33
            },
            'pimozide': {
                'Kmax': 10.07,
                'Ku': 4.576e-5,
                'EC50': 5.601,
                'N': 0.8714,
                'Vhalf': -78.68,
                'Cmax': 0.431
            },
        }
        self.Hill_curve = {
            'dofetilide': {
                'IKr': {
                    'Hill_coef': 0.9,
                    'IC50': 4.9},
                'INaL': {
                    'Hill_coef': 0.3,
                    'IC50': 75316.4},
                'ICaL': {
                    'Hill_coef': 1.2,
                    'IC50': 260.3},
                'INa': {
                    'Hill_coef': 0.9,
                    'IC50': 380.5},
                'Ito': {
                    'Hill_coef': 0.8,
                    'IC50': 18.8},
                'IK1': {
                    'Hill_coef': 0.8,
                    'IC50': 394.3},
                'IKs': {
                    'Hill_coef': 0,
                    'IC50': 0}, },
            'bepridil': {
                'IKr': {
                    'Hill_coef': 0.9,
                    'IC50': 50},
                'INaL': {
                    'Hill_coef': 1.4,
                    'IC50': 1813.9},
                'ICaL': {
                    'Hill_coef': 0.6,
                    'IC50': 2808.1},
                'INa': {
                    'Hill_coef': 1.2,
                    'IC50': 2929.3},
                'Ito': {
                    'Hill_coef': 3.5,
                    'IC50': 8594},
                'IK1': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'IKs': {
                    'Hill_coef': 0.7,
                    'IC50': 28628.3}, },
            'terfenadine': {
                'IKr': {
                    'Hill_coef': 0.6,
                    'IC50': 23},
                'INaL': {
                    'Hill_coef': 0.6,
                    'IC50': 20056},
                'ICaL': {
                    'Hill_coef': 0.7,
                    'IC50': 700.4},
                'INa': {
                    'Hill_coef': 1,
                    'IC50': 4803.2},
                'Ito': {
                    'Hill_coef': 0.3,
                    'IC50': 239960.8},
                'IK1': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'IKs': {
                    'Hill_coef': 0.5,
                    'IC50': 399754}, },
            'cisapride': {
                'IKr': {
                    'Hill_coef': 0.7,
                    'IC50': 10.1},
                'INaL': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'ICaL': {
                    'Hill_coef': 0.4,
                    'IC50': 9258076},
                'INa': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'Ito': {
                    'Hill_coef': 0.2,
                    'IC50': 219112.4},
                'IK1': {
                    'Hill_coef': 0.5,
                    'IC50': 29498},
                'IKs': {
                    'Hill_coef': 0.3,
                    'IC50': 81192862}, },
            'verapamil': {
                'IKr': {
                    'Hill_coef': 1,
                    'IC50': 288},
                'INaL': {
                    'Hill_coef': 1,
                    'IC50': 7028},
                'ICaL': {
                    'Hill_coef': 1.1,
                    'IC50': 201.8},
                'INa': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'Ito': {
                    'Hill_coef': 0.8,
                    'IC50': 13429.2},
                'IK1': {
                    'Hill_coef': 0.3,
                    'IC50': 3.49e8},
                'IKs': {
                    'Hill_coef': 0,
                    'IC50': 0}, },
            'ranolazine': {
                'IKr': {
                    'Hill_coef': 0.9,
                    'IC50': 8270},
                'INaL': {
                    'Hill_coef': 0.9,
                    'IC50': 7884.5},
                'ICaL': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'INa': {
                    'Hill_coef': 1.4,
                    'IC50': 68774},
                'Ito': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'IK1': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'IKs': {
                    'Hill_coef': 0.5,
                    'IC50': 36155020}, },
            'mexiletine': {
                'IKr': {
                    'Hill_coef': 0.9,
                    'IC50': 28880},
                'INaL': {
                    'Hill_coef': 1.4,
                    'IC50': 8956.8},
                'ICaL': {
                    'Hill_coef': 1,
                    'IC50': 38243.6},
                'INa': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'Ito': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'IK1': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'IKs': {
                    'Hill_coef': 0,
                    'IC50': 0}, },
            'quinidine': {
                'IKr': {
                    'Hill_coef': 0.8,
                    'IC50': 992},
                'INaL': {
                    'Hill_coef': 1.3,
                    'IC50': 9417},
                'ICaL': {
                    'Hill_coef': 0.6,
                    'IC50': 51592.3},
                'INa': {
                    'Hill_coef': 1.5,
                    'IC50': 12329},
                'Ito': {
                    'Hill_coef': 1.3,
                    'IC50': 3487.4},
                'IK1': {
                    'Hill_coef': 0.4,
                    'IC50': 39589919},
                'IKs': {
                    'Hill_coef': 1.4,
                    'IC50': 4898.9}, },
            'sotalol': {
                'IKr': {
                    'Hill_coef': 0.8,
                    'IC50': 110600},
                'INaL': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'ICaL': {
                    'Hill_coef': 0.9,
                    'IC50': 7061527},
                'INa': {
                    'Hill_coef': 0.5,
                    'IC50': 1.14e9},
                'Ito': {
                    'Hill_coef': 0.7,
                    'IC50': 43143455},
                'IK1': {
                    'Hill_coef': 1.2,
                    'IC50': 3050260},
                'IKs': {
                    'Hill_coef': 1.2,
                    'IC50': 4221856}, },
            'chlorpromazine': {
                'IKr': {
                    'Hill_coef': 0.8,
                    'IC50': 929.2},
                'INaL': {
                    'Hill_coef': 0.9,
                    'IC50': 4559.6},
                'ICaL': {
                    'Hill_coef': 0.8,
                    'IC50': 8191.9},
                'INa': {
                    'Hill_coef': 2,
                    'IC50': 4535.6},
                'Ito': {
                    'Hill_coef': 0.4,
                    'IC50': 17616711},
                'IK1': {
                    'Hill_coef': 0.7,
                    'IC50': 9269.9},
                'IKs': {
                    'Hill_coef': 0,
                    'IC50': 0}, },
            'ondansetron': {
                'IKr': {
                    'Hill_coef': 0.9,
                    'IC50': 1320},
                'INaL': {
                    'Hill_coef': 1,
                    'IC50': 19180.8},
                'ICaL': {
                    'Hill_coef': 0.8,
                    'IC50': 22551.4},
                'INa': {
                    'Hill_coef': 1,
                    'IC50': 57666.4},
                'Ito': {
                    'Hill_coef': 1,
                    'IC50': 1023378},
                'IK1': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'IKs': {
                    'Hill_coef': 0.7,
                    'IC50': 569807}, },
            'diltiazem': {
                'IKr': {
                    'Hill_coef': 0.9,
                    'IC50': 13150},
                'INaL': {
                    'Hill_coef': 0.7,
                    'IC50': 21868.5},
                'ICaL': {
                    'Hill_coef': 0.7,
                    'IC50': 112.1},
                'INa': {
                    'Hill_coef': 0.7,
                    'IC50': 110859},
                'Ito': {
                    'Hill_coef': 0.2,
                    'IC50': 2.82e9},
                'IK1': {
                    'Hill_coef': 0,
                    'IC50': 0},
                'IKs': {
                    'Hill_coef': 0,
                    'IC50': 0}, }, }


class ProtocolParameters(object):
    """
    To create a library of all the parameters for different protocols,
    especially default pulse time and function name.
    """

    def __init__(self):
        super(ProtocolParameters, self).__init__()

        self.protocols = ['Milnes', 'Pneg80', 'P0', 'P40']
        self.protocol_parameters = {
            'Milnes': {
                'pulse_time': 25e3,
                'function': modelling.ProtocolLibrary().Milnes(25e3),
                'voltage_points': [-80, 0],
            },
            'Pneg80': {
                'pulse_time': 5400,
                'function': modelling.ProtocolLibrary().Pneg80(5400),
                'voltage_points': [-80, -50, 20],
            },
            'P0': {
                'pulse_time': 5400,
                'function': modelling.ProtocolLibrary().P0(5400),
                'voltage_points': [-80, -60, 0],
            },
            'P40': {
                'pulse_time': 5400,
                'function': modelling.ProtocolLibrary().P40(5400),
                'voltage_points': [-80, -60, 40],
            },
        }


class DrugConcentrations(object):
    """
    Create a library for default list of drug concentrations
    """
    def __init__(self):
        super(DrugConcentrations, self).__init__()

        self.drug_compounds = ['dofetilide', 'bepridil', 'terfenadine',
                               'cisapride', 'verapamil', 'ranolazine',
                               'quinidine', 'sotalol', 'chlorpromazine',
                               'ondansetron', 'diltiazem', 'mexiletine',
                               'droperidol']
        self.drug_concentrations = {
            'dofetilide': {
                'coarse': [0, 0.1, 1, 10, 30, 100, 300, 500, 1000],
                'fine': 10.0**np.linspace(-1, 2.5, 20),
                'lit_default': [1, 3, 10, 30]
            },
            'verapamil': {
                'coarse': [0, 0.1, 1, 30, 300, 1000, 10000, 1e5],
                'fine': 10.0**np.linspace(-1, 5, 20),
                'lit_default': [30, 100, 300, 1000]
            },
            'bepridil': {
                'coarse': [0, 0.1, 1, 30, 100, 300, 1000, 10000],
                'fine': 10.0**np.linspace(-1, 5, 20),
                'lit_default': [10, 30, 100, 300]
            },
            'terfenadine': {
                'coarse': [0, 0.1, 1, 10, 30, 100, 300, 500, 1000, 10000],
                'fine': 10.0**np.linspace(-1, 5, 20),
                'lit_default': [3, 10, 30, 100]
            },
            'cisapride': {
                'coarse': [0, 0.1, 1, 10, 30, 100, 300, 500, 1000, 3000],
                'fine': 10.0**np.linspace(-1, 3, 20),
                'lit_default': [1, 10, 100, 300]
            },
            'ranolazine': {
                'coarse': [0, 1, 30, 300, 500, 1000, 10000, 1e5, 1e6],
                'fine': 10.0**np.linspace(1, 5.5, 20),
                'lit_default': [1000, 1e4, 3e4, 1e5]
            },
            'quinidine': {
                'coarse': [0, 1, 30, 300, 500, 1000, 3000, 10000, 1e5],
                'fine': 10.0**np.linspace(-1, 5, 20),
                'lit_default': [100, 300, 1000, 10000]
            },
            'sotalol': {
                'coarse': [0, 1, 30, 100, 300, 1000, 10000, 3e4, 1e5, 3e5,
                           1e6, 1e7],
                'fine': 10.0**np.linspace(-1, 7, 20),
                'lit_default': [1e4, 3e4, 1e5, 3e5]
            },
            'chlorpromazine': {
                'coarse': [0, 1, 30, 300, 500, 1000, 3000, 10000, 1e5],
                'fine': 10.0**np.linspace(-1, 4.5, 20),
                'lit_default': [100, 300, 1000, 3000]
            },
            'ondansetron': {
                'coarse': [0, 1, 30, 300, 500, 1000, 3000, 10000, 1e5, 3e5],
                'fine': 10.0**np.linspace(-1, 5.5, 20),
                'lit_default': [300, 1000, 3000, 1e4]
            },
            'diltiazem': {
                'coarse': [0, 1, 30, 100, 300, 1000, 3000, 10000, 3e4, 1e5,
                           1e6, 1e7],
                'fine': 10.0**np.linspace(-1, 6, 20),
                'lit_default': [3000, 1e4, 3e4, 1e5]
            },
            'mexiletine': {
                'coarse': [0, 1, 30, 100, 300, 1000, 10000, 3e4, 1e5, 1e6,
                           1e7],
                'fine': 10.0**np.linspace(-1, 7, 20),
                'lit_default': [1e4, 3e4, 1e5, 3e5]
            },
        }


class ParameterCategory(object):
    """
    Create a library for each parameter's category ranges
    """
    def __init__(self):
        super(ParameterCategory, self).__init__()

        self.param_names = ['Vhalf', 'Kmax', 'Ku', 'N', 'EC50']

        self.param_ranges = {
            'Vhalf': (-150, -50),
            'Kmax': (30, 1e6),
            'Ku': (5e-3, 7e-2),
            'N': (0.8, 1.2),
            'EC50': (1e3, 1e8)
        }
