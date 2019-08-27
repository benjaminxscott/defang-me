# defang.me

Safely share indicators with other security researchers

## Deployment
TODO - aws with lightsail

TODO - gcp - notes from prior build on appengine?

## Impetus
In computer security, people often email around "indicators", which are things like IP addresses, domain names, URLs, and md5 digests.

There have been [several](https://oasis-open.github.io/cti-documentation/stix/walkthrough) credible [attempts](https://www.misp-project.org/datamodels/) to create machine-parseable formats to share these indicators around in JSON, which are mostly useful for high-throughput organizations like giant banks, NSA NTOC or NATO

Since [nobody can agree](https://xkcd.com/927/) on which format is the best, most security researchers publish indicators [in CSVs or tables](https://www.fireeye.com/blog/threat-research/2018/11/not-so-cozy-an-uncomfortable-examination-of-a-suspected-apt29-phishing-campaign.html) and let the reader sort it out

In practice, people tend to just send indicators around via email or chat. 

Since some of the indicators can be malicious IPs/domains/URLs, there's an informal process called "defanging" which renders them unclickable.

### What is defanging? 

A defanged indicator undergos regex replacement to prevent email clients from parsing it as a URL

The typical defanging process involves one or more transformations:

- replace characters in the protocol e.g. `hXXp://evil.com` or `meow://evil.com` 
- add brackets around periods e.g. `http://evil[.]com` or `1.2.3[.]4`
- Include spaces around periods `http://evil . com`

### So what's the issue?

There are usage problems with the status quo:

- Users have to copy/paste indicators from webpages, PDFs, and email, which is error-prone
- If a list of indicators is updated or modified, every recipient has to generate and apply their own diff (!!)

The defanging process is user-hostile:

- Defanged indicators must be "refanged" in order to be useful
- Defang implementations are inconsistent, requiring manual effort to refang (e.g. "Jeff likes to use `meow:` and Jane likes to use `[.]`)

The defanging process is broken:

- The refanging process [cannot be done via a "regular language" such as regex](https://stackoverflow.com/a/3816749) (note that a regex can be used in some cases)
- Email clients parse and render URLs in different ways (e.g. Gmail will helpfully turn a bare domain into an http link)

