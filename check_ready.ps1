# Pre-Deployment Readiness Check
# Run this before deploying to verify you have everything set up

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host " Pre-Deployment Readiness Check" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

$allGood = $true

# Check Git
Write-Host "[1/5] Checking Git..." -ForegroundColor Yellow
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Host "  ✓ Git installed: $gitVersion" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Git not found" -ForegroundColor Red
        Write-Host "    Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
        $allGood = $false
    }
} catch {
    Write-Host "  ✗ Git not installed" -ForegroundColor Red
    $allGood = $false
}

# Check Node.js
Write-Host ""
Write-Host "[2/5] Checking Node.js..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "  ✓ Node.js installed: $nodeVersion" -ForegroundColor Green
    } else {
        Write-Host "  ✗ Node.js not found" -ForegroundColor Red
        Write-Host "    Download from: https://nodejs.org/" -ForegroundColor Yellow
        $allGood = $false
    }
} catch {
    Write-Host "  ✗ Node.js not installed" -ForegroundColor Red
    $allGood = $false
}

# Check Python
Write-Host ""
Write-Host "[3/5] Checking Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>$null
    if ($pythonVersion) {
        Write-Host "  ✓ Python installed: $pythonVersion" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Python not found (optional - needed for local testing)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "  ⚠ Python not found (optional)" -ForegroundColor Yellow
}

# Check project structure
Write-Host ""
Write-Host "[4/5] Checking project structure..." -ForegroundColor Yellow

if (Test-Path ".\frontend") {
    Write-Host "  ✓ Frontend directory exists" -ForegroundColor Green
} else {
    Write-Host "  ✗ Frontend directory not found" -ForegroundColor Red
    $allGood = $false
}

if (Test-Path ".\backend") {
    Write-Host "  ✓ Backend directory exists" -ForegroundColor Green
} else {
    Write-Host "  ✗ Backend directory not found" -ForegroundColor Red
    $allGood = $false
}

if (Test-Path ".\backend\requirements.txt") {
    Write-Host "  ✓ requirements.txt exists" -ForegroundColor Green
} else {
    Write-Host "  ✗ requirements.txt not found" -ForegroundColor Red
    $allGood = $false
}

if (Test-Path ".\frontend\package.json") {
    Write-Host "  ✓ package.json exists" -ForegroundColor Green
} else {
    Write-Host "  ✗ package.json not found" -ForegroundColor Red
    $allGood = $false
}

# Check deployment files
Write-Host ""
Write-Host "[5/5] Checking deployment files..." -ForegroundColor Yellow

if (Test-Path ".\render.yaml") {
    Write-Host "  ✓ render.yaml exists" -ForegroundColor Green
} else {
    Write-Host "  ⚠ render.yaml not found (optional)" -ForegroundColor Yellow
}

if (Test-Path ".\vercel.json") {
    Write-Host "  ✓ vercel.json exists" -ForegroundColor Green
} else {
    Write-Host "  ⚠ vercel.json not found (optional)" -ForegroundColor Yellow
}

if (Test-Path ".\.gitignore") {
    Write-Host "  ✓ .gitignore exists" -ForegroundColor Green
} else {
    Write-Host "  ⚠ .gitignore not found (recommended)" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
if ($allGood) {
    Write-Host " ✓ All checks passed!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "You're ready to deploy!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Cyan
    Write-Host "  1. Read START_HERE.md" -ForegroundColor White
    Write-Host "  2. Open DEPLOYMENT_STEPS.md" -ForegroundColor White
    Write-Host "  3. Follow the deployment guide" -ForegroundColor White
    Write-Host ""
    Write-Host "Quick deploy:" -ForegroundColor Cyan
    Write-Host "  cd frontend" -ForegroundColor White
    Write-Host "  vercel --prod" -ForegroundColor White
} else {
    Write-Host " ✗ Some checks failed" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Please install missing requirements above." -ForegroundColor Yellow
}
Write-Host ""

# Check if Vercel CLI is installed
Write-Host "Optional: Checking Vercel CLI..." -ForegroundColor Yellow
try {
    $vercelVersion = vercel --version 2>$null
    if ($vercelVersion) {
        Write-Host "  ✓ Vercel CLI installed: $vercelVersion" -ForegroundColor Green
    } else {
        Write-Host "  ⚠ Vercel CLI not installed" -ForegroundColor Yellow
        Write-Host "    Install with: npm install -g vercel" -ForegroundColor Cyan
    }
} catch {
    Write-Host "  ⚠ Vercel CLI not installed" -ForegroundColor Yellow
    Write-Host "    Install with: npm install -g vercel" -ForegroundColor Cyan
}

Write-Host ""

