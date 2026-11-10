from setuptools import find_packages, setup

package_name = "otas_telemetry"

setup(
    name=package_name,
    version="0.1.0",
    packages=find_packages(exclude=["test"]),
    data_files=[
        (
            "share/ament_index/resource_index/packages",
            ["resource/" + package_name],
        ),
        ("share/" + package_name, ["package.xml"]),
    ],
    install_requires=["setuptools"],
    zip_safe=True,
    maintainer="OTAS Software Team",
    maintainer_email="maintainer@example.com",
    description="T1 telemetry and heartbeat publisher for OTAS.",
    license="Apache-2.0",
    tests_require=["pytest"],
    entry_points={
        "console_scripts": [
            "telemetry_publisher = "
            "otas_telemetry.telemetry_publisher:main",
        ],
    },
)
