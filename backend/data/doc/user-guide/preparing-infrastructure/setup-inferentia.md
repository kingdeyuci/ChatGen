# Setup Inferentia

AWS Neuron is the SDK used to run deep learning workloads on AWS Inferentia and AWS Trainium based instances. It supports customers in their end-to-end ML development lifecycle to build new models, train and optimize these models, and then deploy them for production. ([source][inferentia desc])

Workloads that require to use the AWS Inferentia NEURON Accelerator must specify a `HAS-SETUP-INFERENTIA-NEURON` label.

## System Setup

- To setup the Inferentia neuron runtime package - see [Get Started with Neuron][get started].

## Node Labels

The following node label is available on the worker node:

- `HAS-SETUP-INFERENTIA-NEURON=yes`: Optional


[inferentia desc]: https://awsdocs-neuron.readthedocs-hosted.com/en/latest/index.html
[get started]: https://awsdocs-neuron.readthedocs-hosted.com/en/latest/general/quick-start/index.html#neuron-quickstart
