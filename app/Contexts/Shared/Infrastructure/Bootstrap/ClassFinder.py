import importlib
import inspect
import logging
import os

import toml  # type: ignore


class ClassFinder:
    _logger: logging.Logger = logging.getLogger(__name__)

    @staticmethod
    def find[T](base_class: type[T], suffix: str, base_path: str | None = None) -> list[type[T]]:  # type: ignore[type-arg]
        """
        Gets all classes that extend from a base class and have a specific suffix.
        Searches in packages defined in pyproject.toml using setuptools configuration.
        Args:
            base_class (Type): The base class that classes must extend from
            suffix (str): The suffix that classes must have
        Returns:
            List[Type]: List of classes that meet the criteria
        """
        classes = []
        # Read pyproject.toml to get package directory
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.abspath(
            os.path.join(current_dir, "..", "..", "..", "..", "..")
        )
        pyproject_path = os.path.join(project_root, "pyproject.toml")

        ClassFinder._logger.debug(f"Searching in project root: {project_root}")
        ClassFinder._logger.debug(f"Looking for pyproject.toml at: {pyproject_path}")

        if not os.path.exists(pyproject_path):
            raise FileNotFoundError(f"pyproject.toml not found at {pyproject_path}")

        pyproject = toml.load(pyproject_path)

        # Get package directory from setuptools configuration
        package_dir = (
            pyproject.get("tool", {})
            .get("setuptools", {})
            .get("package-dir", {})
            .get("", "app")
        )
        package_path = os.path.join(project_root, package_dir)

        ClassFinder._logger.debug(
            f"Package directory from pyproject.toml: {package_dir}"
        )
        ClassFinder._logger.debug(f"Full package path: {package_path}")

        if not os.path.exists(package_path):
            raise FileNotFoundError(f"Package directory not found at {package_path}")

        for root, _, files in os.walk(package_path):
            for file in files:
                if file.endswith(f"{suffix}.py"):
                    module_path = os.path.join(root, file)
                    relative_path = os.path.relpath(module_path, project_root)
                    module_name = relative_path.replace(os.sep, ".")[
                        :-3
                    ]  # Remove '.py'

                    ClassFinder._logger.debug(f"Found potential module: {module_name}")

                    try:
                        module = importlib.import_module(module_name)
                        for name, obj in inspect.getmembers(module):
                            if (
                                inspect.isclass(obj)
                                and not inspect.isabstract(obj)
                                and issubclass(obj, base_class)
                                and obj != base_class
                            ):
                                ClassFinder._logger.debug(
                                    f"Found matching class: {name}"
                                )
                                classes.append(obj)
                    except Exception as e:
                        ClassFinder._logger.error(
                            f"Error importing module {module_name}: {e}"
                        )
                        raise e

        ClassFinder._logger.debug(f"Total classes found: {len(classes)}")
        return classes
