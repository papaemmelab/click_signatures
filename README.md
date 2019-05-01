# click_signatures

[![travis badge][travis_badge]][travis_base]
[![codecov badge][codecov_badge]][codecov_base]
[![docker badge][docker_badge]][docker_base]
[![docker badge][automated_badge]][docker_base]
[![code formatting][black_badge]][black_base]

✍️ Run MutationalPattern on single sample SNVs.

## Usage

Run with [containers][docker_base]:

        # docker usage
        docker run papaemmelab/click_signatures --help

        # singularity usage
        singularity run docker://papaemmelab/click_signatures --help

See [docker2singularity] if you want to use a [singularity] image instead of using the `docker://` prefix.

### Example

    docker run papaemmelab/click_signatures \
        --outdir {outdir} \
        --id {sample id} \
        --vcf {SNP vcf file} \
        --sigprob {signature probability file}

## Contributing

Contributions are welcome, and they are greatly appreciated, check our [contributing guidelines](.github/CONTRIBUTING.md)!

## Credits

This package was created using [Cookiecutter] and the
[papaemmelab/cookiecutter-toil] project template.

[`--batchSystem`]: http://toil.readthedocs.io/en/latest/developingWorkflows/batchSystem.html?highlight=BatchSystem
[automated_badge]: https://img.shields.io/docker/cloud/automated/papaemmelab/click_signatures.svg
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black_base]: https://github.com/ambv/black
[codecov_badge]: https://codecov.io/gh/papaemmelab/click_signatures/branch/master/graph/badge.svg
[codecov_base]: https://codecov.io/gh/papaemmelab/click_signatures
[cookiecutter]: https://github.com/audreyr/cookiecutter
[docker_badge]: https://img.shields.io/docker/cloud/build/papaemmelab/click_signatures.svg
[docker_base]: https://hub.docker.com/r/papaemmelab/click_signatures
[docker2singularity]: https://github.com/singularityware/docker2singularity
[papaemmelab/cookiecutter-toil]: https://github.com/papaemmelab/cookiecutter-toil
[singularity]: http://singularity.lbl.gov/
[travis_badge]: https://img.shields.io/travis/papaemmelab/click_signatures.svg
[travis_base]: https://travis-ci.org/papaemmelab/click_signatures
