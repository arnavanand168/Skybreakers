# 🚀 United Airlines Flight Difficulty Dashboard - Deployment Guide

## Overview
This guide provides step-by-step instructions for deploying the United Airlines Flight Difficulty Dashboard to various cloud platforms.

## 📁 Project Structure
```
skyhack/
├── app.py                      # Flask web application
├── requirements_flask.txt      # Flask dependencies
├── templates/                  # HTML templates
│   ├── base.html
│   ├── dashboard.html
│   └── about.html
├── static/                    # Static files
│   ├── css/style.css
│   └── js/dashboard.js
├── skyhack.db                 # SQLite database
├── vercel.json                # Vercel configuration
├── Procfile                   # Heroku configuration
└── DEPLOYMENT_GUIDE.md        # This file
```

## 🌐 Deployment Options

### Option 1: Vercel (Recommended for Static Sites)

#### Prerequisites
- GitHub account
- Vercel account

#### Steps
1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Initialize Vercel Project**
   ```bash
   cd skyhack
   vercel
   ```

3. **Configure Environment**
   ```bash
   vercel env add DATABASE_PATH
   # Enter: skyhack.db
   ```

4. **Deploy**
   ```bash
   vercel --prod
   ```

#### Alternative: Direct GitHub Integration
1. Push your code to GitHub
2. Connect GitHub repository to Vercel
3. Auto-deploy on every push

### Option 2: Heroku

#### Prerequisites
- Heroku account
- Heroku CLI installed

#### Steps
1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku
   
   # Or download from heroku.com
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku App**
   ```bash
   heroku create united-flight-dashboard
   ```

4. **Set Environment Variables**
   ```bash
   heroku config:set DATABASE_PATH=skyhack.db
   heroku config:set FLASK_ENV=production
   ```

5. **Deploy**
   ```bash
   git add .
   git commit -m "Deploy to Heroku"
   git push heroku main
   ```

### Option 3: PythonAnywhere

#### Prerequisites
- PythonAnywhere account (free tier available)

#### Steps
1. **Upload Files**
   - Upload all project files to PythonAnywhere
   - Ensure `skyhack.db` is in the root directory

2. **Install Dependencies**
   ```bash
   pip3.10 install --user flask pandas plotly numpy
   ```

3. **Configure WSGI File**
   Create `mysite/wsgi.py`:
   ```python
   import sys
   import os
   
   path = '/home/yourusername/skyhack'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

4. **Set Web App URL**
   - Use provided URL or custom domain

### Option 4: Railway

#### Steps
1. **Connect GitHub Repository**
   - Push code to GitHub
   - Connect Railway to GitHub repo

2. **Set Environment Variables**
   ```
   DATABASE_PATH=skyhack.db
   PORT=5000
   ```

3. **Auto-Deploy**
   - Railway automatically detects Flask app
   - Deploys on every push

## 🔧 Configuration

### Environment Variables
```bash
DATABASE_PATH=skyhack.db
FLASK_ENV=production
SECRET_KEY=your-secret-key-change-this
PORT=5000
```

### Database Considerations
- **SQLite**: Works for small-to-medium deployments
- **PostgreSQL**: Recommended for production (requires migration)

## 📱 Mobile Compatibility
The dashboard is fully responsive and works on:
- ✅ Desktop browsers
- ✅ Mobile devices
- ✅ Tablets

## 🔒 Security Features
- CSRF protection
- Input validation
- Secure headers
- Error handling

## 📊 Performance Optimization
- Chart caching
- Database query optimization
- Responsive image loading
- CDN integration ready

## 🧪 Testing Deployment

### Health Check Endpoint
```
GET /api/health
Response: {"status": "healthy", "timestamp": "...", "database_exists": true}
```

### Manual Testing Steps
1. ✅ Dashboard loads
2. ✅ Charts display correctly
       3. ✅ Data tables populate
4. ✅ API endpoints respond
5. ✅ Mobile responsiveness
6. ✅ Auto-refresh works

## 🚨 Troubleshooting

### Common Issues

#### Database Not Found
```
Solution: Ensure skyhack.db is uploaded with correct permissions
```

#### Charts Not Loading
```
Solution: Check Plotly.js CDN connection and API endpoints
```

#### Static Files 404
```
Solution: Verify static files directory structure and Vercel/Heroku config
```

#### Memory Issues
```
Solution: Optimize queries and consider database migration
```

## 📈 Monitoring

### Performance Metrics
- Response time: < 2 seconds
- Memory usage: ~128MB typical
- Database queries: Optimized with indexes

### Analytics Integration
Ready for:
- Google Analytics
- Mixpanel
- Custom event tracking

## 🔄 Updates & Maintenance

### Auto-Deploy Setup
1. Connect GitHub webhook
2. Set up CI/CD pipeline
3. Configure branch protection

### Database Backups
- Automated backups recommended
- Version control for schema changes

## 💰 Cost Estimates

| Platform | Free Tier | Paid Plans |
|----------|-----------|------------|
| Vercel | 100GB bandwidth/month | $20/month |
| Heroku | 550 hours/month | $7/month |
| PythonAnywhere | 3 web apps | $5/month |
| Railway | 500 hours/month | $5/month |

## 🎯 Next Steps

After deployment:
1. Set up monitoring
2. Configure backups
3. Setup domain name
4. Implement authentication
5. Add API rate limiting

## 📞 Support

For deployment issues:
- Check platform documentation
- Review error logs
- Test locally first
- Monitor resource usage

---

**Ready to deploy your United Airlines Flight Difficulty Dashboard! 🛫**
