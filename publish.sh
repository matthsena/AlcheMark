echo "Cleaning previous builds..."
rm -rf dist/ build/ *.egg-info

echo "Building package..."
python -m build

echo "Checking package..."
twine check dist/*

echo "Ready to upload to PyPI"
echo "To upload to Test PyPI, run: twine upload --repository testpypi dist/*"
echo "To upload to PyPI, run: twine upload dist/*"

read -p "Do you want to upload to Test PyPI? (y/n): " choice
if [[ $choice == "y" || $choice == "Y" ]]; then
    twine upload --repository testpypi dist/*
    echo "Package uploaded to Test PyPI."
    echo "You can install it with: pip install --index-url https://test.pypi.org/simple/ alchemark-ai"
fi

read -p "Do you want to upload to PyPI? (y/n): " choice
if [[ $choice == "y" || $choice == "Y" ]]; then
    twine upload dist/*
    echo "Package uploaded to PyPI."
    echo "You can install it with: pip install alchemark-ai"
fi 