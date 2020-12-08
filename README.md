# XJDF & JDF Specifications
JDF (Job Definition Format) is an interchange data format to be used by a system of administrative and implementation-oriented components, which together produce printed products. It provides the means to describe print Jobs in terms of the products eventually to be created, as well as in terms of the Processes needed to create those products. The format provides a mechanism to explicitly specify the controls needed by each Process, which might be specific to the Devices that will execute the Processes.  

## Download
Here are the direct links to the appropriate releases at github.com:
- [XJDF Specificaion 2.1](https://github.com/cip4/JDF-Specification/releases/download/2.1/XJDF-Specification-2.1.pdf)
- [XJDF Specificaion 1.7](https://github.com/cip4/JDF-Specification/releases/download/1.7/XJDF-Specification-1.7.pdf)

More released versions can be found on the [releases page](https://github.com/cip4/JDF-Specification/releases).
  
## Issue Tracking
For issue tracking please refer to [CIP4 JIRA](https://jira.cip4.org/projects/JDF/summary).  

## Developer Notes
### Build Artefacts
Each build process produces a single artefacts (zip). This contains the resultant PDFs for each type of build.  

### Build Process
CI builds are triggered by any 'push' to the [MASTER] branch.<br/>
There is an option to trigger this build manually in the event that an automated CI build fails due to issues with the build process.

Release builds are triggered by adding a git tag to a commit. The value of tag will be used as the document identifier on both the cover and in the resulting artefact file name.<br/>
For example use a tag of 'DRAFT-IP4' or '2.1'.<br/>
There is also an option to trigger this build manually.
