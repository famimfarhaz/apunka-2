# 🚀 KPI GPT Deployment Guide for PythonAnywhere

## Overview
This guide will help you deploy your KPI GPT RAG system to PythonAnywhere, a cloud-based Python hosting platform.

## 📋 Prerequisites

### 1. PythonAnywhere Account
- Sign up at [pythonanywhere.com](https://www.pythonanywhere.com)
- Free account includes: 512MB storage, 100 seconds CPU/day, 1 web app
- Paid accounts offer more resources and multiple web apps

### 2. Groq API Key
- Sign up at [console.groq.com](https://console.groq.com)
- Generate an API key from the Keys section
- Keep this key secure - you'll need it for configuration

## 🚀 Step-by-Step Deployment

### Step 1: Upload Your Files

1. **Log in to PythonAnywhere**
   - Go to your dashboard

2. **Open File Manager**
   - Click on "Files" in the dashboard
   - You'll be in your home directory (`/home/yourusername/`)

3. **Create Project Directory**
   - Navigate to or create the `mysite` directory
   - This is where your web app files will live

4. **Upload Files**
   - Upload all files from this deployment package to `/home/yourusername/mysite/`
   - You can use the upload button or drag-and-drop
   - **Important**: Make sure to upload the `templates/` and `static/` folders as well

### Step 2: Set Up the Web Application

1. **Go to Web Tab**
   - Click on "Web" in the main navigation
   - If you don't have a web app yet, click "Add a new web app"

2. **Create New Web App**
   - Choose "Flask" as the framework
   - Select Python 3.10 (recommended)
   - Use the default project name or choose your own

3. **Configure Source Code**
   - In the "Code" section, set the source code directory to: `/home/yourusername/mysite`
   - **Important**: Replace `yourusername` with your actual PythonAnywhere username

4. **Update WSGI Configuration**
   - First, rename `flask_app.py` to match your username: `yourusername_flask_app.py`
   - In the Web tab, update the "WSGI configuration file" to point to your renamed file
   - Or edit the existing WSGI file to import from your app

### Step 3: Install Dependencies

1. **Open a Bash Console**
   - Go to "Consoles" → "Bash"
   - This gives you a command-line interface

2. **Navigate to Your Project**
   ```bash
   cd ~/mysite
   ```

3. **Create Virtual Environment** (if not already done)
   ```bash
   mkvirtualenv --python=/usr/bin/python3.10 mysite-virtualenv
   ```

4. **Activate Virtual Environment**
   ```bash
   workon mysite-virtualenv
   ```

5. **Install Requirements**
   ```bash
   pip install -r requirements.txt
   ```
   
   **Note**: This may take several minutes. Some packages might take longer to compile.

### Step 4: Configure Environment Variables

1. **Create Environment File**
   ```bash
   cp .env.template .env
   nano .env
   ```

2. **Edit Environment Variables**
   - Replace `your_groq_api_key_here` with your actual Groq API key
   - Replace `yourusername` with your actual PythonAnywhere username
   - Update other variables as needed

3. **Important Variables to Set**:
   ```
   GROQ_API_KEY=your_actual_groq_api_key
   SECRET_KEY=your-unique-secret-key
   FLASK_ENV=production
   PROJECT_ROOT=/home/yourusername/mysite
   ```

### Step 5: Update Web App Configuration

1. **Go Back to Web Tab**
   - Update the virtualenv path if you created one: `/home/yourusername/.virtualenvs/mysite-virtualenv`

2. **Set Static Files** (if you have CSS/JS)
   - Static URL: `/static/`
   - Static Directory: `/home/yourusername/mysite/static/`

3. **Reload Web App**
   - Click the green "Reload yourusername.pythonanywhere.com" button

### Step 6: Test Your Application

1. **Visit Your Site**
   - Go to `https://yourusername.pythonanywhere.com`
   - Replace `yourusername` with your actual username

2. **Check for Errors**
   - If the site doesn't load, check the Error Log in the Web tab
   - Common issues: import errors, missing dependencies, wrong file paths

3. **Test Functionality**
   - Try asking a sample question like "Who is the principal of KPI?"
   - Wait for the system to initialize (may take a few moments on first load)

## 🔧 Troubleshooting

### Common Issues and Solutions

1. **Import Errors**
   - Check that all files are uploaded to the correct directory
   - Verify the WSGI file path is correct
   - Ensure virtual environment is set up properly

2. **Dependencies Not Found**
   - Make sure you activated the virtual environment before installing requirements
   - Some packages might need manual installation: `pip install package-name`

3. **Groq API Errors**
   - Verify your API key is correct in the .env file
   - Check that your Groq account has available credits

4. **File Permission Issues**
   - Ensure uploaded files have proper permissions
   - The application should be able to create the vector database

5. **Memory Issues (Free Account)**
   - Free accounts have limited memory
   - Consider optimizing or upgrading to a paid plan for better performance

### Checking Logs

1. **Error Log**: In Web tab → "Log files" → Error log
2. **Server Log**: In Web tab → "Log files" → Server log
3. **Console Debugging**: Use Bash console to run Python commands and test imports

## 📊 Performance Tips

### Free Account Optimization
- The system initializes on first request (may be slow initially)
- Consider upgrading to a paid plan for better performance
- Free accounts have CPU seconds limits - paid plans have better allowances

### Paid Account Benefits
- More CPU seconds per day
- Always-on tasks for background processing
- Multiple web apps
- More storage space
- SSH access

## 🔄 Updates and Maintenance

### Updating Your Application
1. Upload new files to replace old ones
2. Reinstall requirements if they changed: `pip install -r requirements.txt`
3. Reload the web app from the Web tab

### Monitoring
- Check error logs regularly
- Monitor CPU usage (especially on free accounts)
- Keep an eye on storage usage

## 📞 Support

### Getting Help
1. **PythonAnywhere Help**: Check their help pages and forums
2. **Error Messages**: Copy exact error messages when seeking help
3. **Log Files**: Error logs contain detailed information about issues

### Useful PythonAnywhere Resources
- [PythonAnywhere Help](https://help.pythonanywhere.com/)
- [Flask Deployment Guide](https://help.pythonanywhere.com/pages/Flask/)
- [Debugging Guide](https://help.pythonanywhere.com/pages/DebuggingImportError/)

## ✅ Success Checklist

- [ ] PythonAnywhere account created
- [ ] Groq API key obtained
- [ ] All files uploaded to `/home/yourusername/mysite/`
- [ ] Virtual environment created and activated
- [ ] Requirements installed successfully
- [ ] Environment variables configured
- [ ] WSGI file renamed and configured
- [ ] Web app settings updated
- [ ] Application loads without errors
- [ ] Sample queries work correctly

## 🎉 Congratulations!

Once all steps are complete, your KPI GPT should be live and accessible at:
`https://yourusername.pythonanywhere.com`

The system will initialize on the first request and will be ready to answer questions about Khulna Polytechnic Institute!
