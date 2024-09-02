# Component's README

Each workload should have a README with the required instructions.

## Sections

The workload README should have the following sections:
- Introduction: Introduce the workload and any background information.
- Test Case: Describe the test cases.
- Configuration: Describe the workload configuration parameters.
- Execution: Show some examples of how to run the workload.
- KPI: Describe the KPI definitions and the meanings of the values.
- [Performance BKM][Performance BKM]: Describe system setup and any performance tunning tips.
- [Index Info][Index Info]: List the workload indexing information.
- Validation Notes: This section is auto-inserted by the validation team. New workload should remove this section.
- See Also: Add any workload-related references.

The dummy workload [README](../../../workload/dummy/README.md) for reference.

## Performance BKM

It is recommended to include (but not limited to) the following information in the Performance BKM section:
- The minimum system setup (and the corresponding testcase).
- The recommended system setup (and the corresponding test case).
- Workload parameter tuning guidelines.
- Links to any performance report(s).

## Index Info

The following indexing information must be provided: 

- Name: The workload friendly name. For example: `TPC-DS Spark`.
- Category: The workload category: one of `DataServices`, `ML/DL/AI`, `HPC`, `Media`, `Networking`, `Synthetic`, `uServices`.
- Platform: A list of supported [platform][platform] names, separated by `,`. For example: `ICX`, `SPR`, `GENOA`.
- Keywords: A list of workload related keywords, separated by `,`. Keywords should not contain any whitespace. For example: `Ghost`,`Nodejs`,`WebServer`.
- Permission: A list of access-controlled repositories, separated by `,`. For example: https://github.com/intel-sandbox/example-repo. Leave empty if no additional permissions are needed.
- Stage1 Contact: A list of stage 1 workload developers contact names, separated by `;`. For example: John Cook; Adam Kovalsky.
- Stage2 Contact: A list of stage 2 workload experts contact names, separated by `;`. As above.

[Performance BKM]: #performance-bkm
[Index Info]: #index-info
[platform]: ../../../workload/platforms