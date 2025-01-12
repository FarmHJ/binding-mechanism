#
# Compute the APD90 differences between the AP-SD model and the AP-CS model
# for all synthetic drug.
#

import myokit
import numpy as np
import os
import pandas as pd

import modelling

# Define directories to save simulation data
data_dir = '../simulation_data/'

# Load current model and set Milnes' protocol
model = '../math_model/ohara-cipa-v1-2017-IKr-opt.mmt'
model, _, x = myokit.load(model)
drug_model = modelling.BindingKinetics(model)

protocol_params = modelling.ProtocolParameters()
protocol = protocol_params.protocol_parameters['Milnes']['function']
drug_model.protocol = protocol

# Load AP model and set current protocol
APmodel = '../math_model/ohara-cipa-v1-2017-opt.mmt'
APmodel, _, x = myokit.load(APmodel)
AP_model = modelling.BindingKinetics(APmodel, current_head='ikr')
pulse_time = 1000
AP_model.protocol = modelling.ProtocolLibrary().current_impulse(pulse_time)
base_conductance = APmodel.get('ikr.gKr').value()

# Define constants for simulations
offset = 50
save_signal = 2
repeats = 1000
APD_points = 20

# Get list of synthetic drug
param_lib = modelling.BindingParameters()
drug_list = param_lib.drug_compounds

# Get name of parameters
SA_model = modelling.SensitivityAnalysis()
param_names = SA_model.param_names


def param_evaluation(param_values, drug):

    # Define parameter values of synthetic drug
    print('Running for drug: ', drug)
    orig_half_effect_conc = param_values['EC50'][0]
    param_values['EC50'][0] = 1
    ComparisonController.drug_param_values = param_values

    # Calculate the normalising constant
    Hill_n = param_values['N'][0]
    norm_constant = np.power(orig_half_effect_conc, 1 / Hill_n)

    # Compute Hill curve of the synthetic drug with the SD model
    Hill_curve_coefs, drug_conc_Hill, peaks_norm = \
        ComparisonController.compute_Hill(drug_model,
                                          norm_constant=norm_constant,
                                          parallel=False)
    # The parameters of Hill curve are based on the normalised drug
    # concentration.
    # Hill coefficient remains the same but IC50 -> IC50/EC50

    # Define drug concentration range similar to the drug concentration used
    # to infer Hill curve
    drug_conc_AP = 10**np.linspace(np.log10(drug_conc_Hill[1]),
                                   np.log10(max(drug_conc_Hill)),
                                   APD_points)

    if isinstance(Hill_curve_coefs, str):
        Hill_curve_coefs = [float("nan")] * 2
        APD_trapping = [float("Nan")] * APD_points
        APD_conductance = [float("Nan")] * APD_points
        RMSError = float("Nan")
        MAError = float("Nan")
    else:
        # Simulate APs and APD90s of the AP-SD model and the AP-CS model
        APD_trapping, APD_conductance, drug_conc_AP = \
            ComparisonController.APD_sim(
                AP_model, Hill_curve_coefs, drug_conc=drug_conc_AP,
                EAD=True)

        # Calculate RMSD and MD of simulated APD90 of the two models
        RMSError = ComparisonController.compute_RMSE(APD_trapping,
                                                     APD_conductance)
        MAError = ComparisonController.compute_ME(APD_trapping,
                                                  APD_conductance)

    # Create dataframe to save results
    conc_Hill_ind = ['conc_' + str(i) for i, _ in
                     enumerate(drug_conc_Hill)]
    conc_AP_ind = ['conc_' + str(i) for i, _ in enumerate(drug_conc_AP)]
    index_dict = {'drug': ['drug'],
                  'drug_conc_Hill': conc_Hill_ind,
                  'peak_current': conc_Hill_ind,
                  'Hill_curve': ['Hill_coef', 'IC50'],
                  'param_values': param_names, 'drug_conc_AP': conc_AP_ind,
                  'APD_trapping': conc_AP_ind,
                  'APD_conductance': conc_AP_ind, 'RMSE': ['RMSE'],
                  'ME': ['ME']}
    all_index = [(i, j) for i in index_dict.keys() for j in index_dict[i]]
    index = pd.MultiIndex.from_tuples(all_index)

    param_values['EC50'][0] = orig_half_effect_conc
    big_df = pd.DataFrame(
        [drug] + drug_conc_Hill + list(peaks_norm) + list(Hill_curve_coefs) +
        list(param_values.values[0]) + list(drug_conc_AP) + APD_trapping +
        APD_conductance + [RMSError] + [MAError], index=index)

    return big_df


# Determine completed simulations so that same simulations are not repeated
filename = 'SA_alldrugs.csv'
if os.path.exists(data_dir + filename):
    results_df = pd.read_csv(data_dir + filename, header=[0, 1], index_col=[0],
                             skipinitialspace=True)
    ran_drugs = results_df['drug']['drug'].values
else:
    ran_drugs = []

drug_list = [i for i in drug_list if i not in ran_drugs]

first_iter = True
for drug in drug_list:

    # Get parameter values of each synthetic drug
    Vhalf = param_lib.binding_parameters[drug]['Vhalf']
    Kmax = param_lib.binding_parameters[drug]['Kmax']
    Ku = param_lib.binding_parameters[drug]['Ku']
    Hill_n = param_lib.binding_parameters[drug]['N']
    half_effect_conc = param_lib.binding_parameters[drug]['EC50']

    all_params = [Vhalf, Kmax, Ku, Hill_n, half_effect_conc]

    # Define parameter values input to the system
    orig_param_values = pd.DataFrame(all_params, index=param_names)
    orig_param_values = orig_param_values.T
    ComparisonController = modelling.ModelComparison(orig_param_values)

    # Evaluate the RMSD and MD between APD90s of a synthetic drug from the
    # AP-SD model and the AP-CS model
    if not os.path.exists(data_dir + filename):
        results_df = param_evaluation(orig_param_values, drug)
        results_df = results_df.T
        first_iter = False
    else:
        results_df = pd.read_csv(data_dir + filename, header=[0, 1],
                                 index_col=[0], skipinitialspace=True)
        big_df = param_evaluation(orig_param_values, drug)
        results_df = pd.concat([results_df, big_df.T])

    results_df.to_csv(data_dir + filename)
