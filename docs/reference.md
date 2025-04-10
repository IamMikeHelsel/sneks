# Sneks Repository Reference

## Useful Commands

### Git Commands

```bash
# Clone the repository
git clone https://github.com/username/sneks.git

# Switch branch
git checkout <branch-name>

# Create and switch to a new branch
git checkout -b <new-branch-name>

# Update your local repository
git pull origin <branch-name>

# Stage changes
git add .

# Commit changes
git commit -m "Your commit message"

# Push changes
git push origin <branch-name>
```

### Python Project Commands

```bash
# Create a virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Activate virtual environment (Linux/Mac)
source venv/bin/activate

# Install in development mode
pip install -e .

# Run the game
sneks
# or
python main.py

# Run tests
pytest

# Build distribution packages
python setup.py sdist bdist_wheel

# Install from local build
pip install dist/sneks-0.1.0-py3-none-any.whl
```

## Build Steps

1. **Prerequisites:**
   - Python 3.6 or higher
   - pip (Python package manager)
   - Git

2. **Initial Setup:**
   ```bash
   # Clone the repository
   git clone https://github.com/username/sneks.git
   cd sneks
   
   # Install dependencies
   npm install
   ```

3. **Development Build:**
   ```bash
   # Start the development server
   npm run dev
   ```
   The development server should now be running at http://localhost:3000 (or another configured port)

4. **Production Build:**
   ```bash
   # Create optimized production build
   npm run build
   
   # Start production server (if applicable)
   npm start
   ```

5. **Testing:**
   ```bash
   # Run all tests
   npm test
   
   # Run specific test suite
   npm test -- -t "test-name"
   ```

6. **Deployment:**
   - Automated deployment may be set up with CI/CD pipelines
   - Manual deployment instructions vary based on hosting platform

## Project Structure

```
sneks/
├── docs/            # Documentation files
├── src/             # Source code
├── tests/           # Test files
├── public/          # Static assets
├── package.json     # Project dependencies and scripts
├── README.md        # Project overview
└── ...
```

## Troubleshooting

- If you encounter dependency issues, try deleting `node_modules` folder and `package-lock.json` (or `yarn.lock`), then run `npm install` again
- For build errors, check the console output for specific error messages
- Ensure you're using the correct Node.js version as specified in `.nvmrc` or project documentation

## Additional Resources

- [Project Wiki](https://github.com/username/sneks/wiki)
- [Issue Tracker](https://github.com/username/sneks/issues)
- [Contribution Guidelines](https://github.com/username/sneks/blob/main/CONTRIBUTING.md)
