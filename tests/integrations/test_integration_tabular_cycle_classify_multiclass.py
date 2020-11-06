#!/usr/bin/env python

####################
# Required Modules #
####################

# Generic/Built-in
import logging

# Libs


# Custom


##################
# Configurations #
##################


#############################################################################
# Integration Tests - Tabular Federated Cycle for MULTICLASS CLASSIFICATION #
#############################################################################

def test_integration_tabular_classify_cycle(
    driver, 
    tabular_classify_cycle_multiclass_payloads
):

    project_payload = tabular_classify_cycle_multiclass_payloads['project']
    project_create_resp = driver.projects.create(**project_payload)
    assert project_create_resp['status'] in [200, 201]

    expt_payloads = tabular_classify_cycle_multiclass_payloads['experiment']
    for expt_payload in expt_payloads:
        expt_create_resp = driver.experiments.create(**expt_payload)
        assert expt_create_resp['status'] in [200, 201]

    run_payloads = tabular_classify_cycle_multiclass_payloads['run']
    for run_payload in run_payloads:
        run_create_resp = driver.runs.create(**run_payload)
        assert run_create_resp['status'] in [200, 201]

    participant_payloads = tabular_classify_cycle_multiclass_payloads['participant']
    for ppt_payload in participant_payloads:
        participant_create_resp = driver.participants.create(**ppt_payload)
        assert participant_create_resp['status'] in [200, 201]

    registration_payloads = tabular_classify_cycle_multiclass_payloads['registration']
    for reg_payload in registration_payloads:
        registration_create_resp = driver.registrations.create(**reg_payload)
        assert registration_create_resp['status'] in [200, 201]

    tag_payloads = tabular_classify_cycle_multiclass_payloads['tag']
    for tag_payload in tag_payloads:
        tag_create_resp = driver.tags.create(**tag_payload)
        assert tag_create_resp['status'] in [200, 201]

    alignment_payload = tabular_classify_cycle_multiclass_payloads['alignment']
    alignment_create_resp = driver.alignments.create(**alignment_payload)
    assert alignment_create_resp['status'] in [200, 201]

    model_payloads = tabular_classify_cycle_multiclass_payloads['model']
    for model_payload in model_payloads:
        model_create_resp = driver.models.create(**model_payload)
        assert model_create_resp['status'] in [200, 201]

    validate_payloads = tabular_classify_cycle_multiclass_payloads['validation']
    for validate_payload in validate_payloads:
        validate_create_resp = driver.validations.create(**validate_payload)
        assert validate_create_resp['status'] in [200, 201]

    predict_payloads = tabular_classify_cycle_multiclass_payloads['prediction']
    for predict_payload in predict_payloads:
        predict_create_resp = driver.predictions.create(**predict_payload)
        assert predict_create_resp['status'] in [200, 201]
