# XJDF & JDF Specifications
This is the documentation repository for the CIP4 JDF and XJDF Specifications.

<br />

## Issue Tracking
TBD

<br />


### Build Artefacts
Each build process produces a single artefacts (zip). This contains the resultant PDFs for each type of build.

### Build Process

CI builds are triggered by any 'push' to the [MASTER] branch.<br/>
There is an option to trigger this build manually in the event that an automated CI build fails due to issues with the build process.

Release builds are triggered by adding a git tag to a commit. The value of tag will be used as the document identifier on both the cover and in the resulting artefact file name.<br/>
For example use a tag of 'Draft-IP-4' or 'Version 2.1 Final'.<br/>
There is also an option to trigger this build manually.
