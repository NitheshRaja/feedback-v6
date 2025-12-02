# Pre-Deployment Readiness Check
Write-Host ""
Write-Host "========================================"
Write-Host " Pre-Deployment Readiness Check"
Write-Host "========================================"
Write-Host ""

$allGood = $true

# Check Git
Write-Host "[1/5] Checking Git..."
try {
    $gitVersion = git --version 2>$null
    if ($gitVersion) {
        Write-Host "  OK Git installed: $gitVersion"
    } else {
        Write-Host "  ERROR Git not found"
        $allGood = $false
    }
} catch {
    Write-Host "  ERROR Git not installed"
    $allGood = $false
}

# Check Node.js
Write-Host ""
Write-Host "[2/5] Checking Node.js..."
try {
    $nodeVersion = node --version 2>$null
    if ($nodeVersion) {
        Write-Host "  OK Node.js installed: $nodeVersion"
    } else {
        Write-Host "  ERROR Node.js not found"
        $allGood = $false
    }
} catch {
    Write-Host "  ERROR Node.js not installed"
    $allGood = $false
}

# Check project structure
Write-Host ""
Write-Host "[3/5] Checking project structure..."

if (Test-Path ".\frontend") {
    Write-Host "  OK Frontend directory exists"
} else {
    Write-Host "  ERROR Frontend directory not found"
    $allGood = $false
}

if (Test-Path ".\backend") {
    Write-Host "  OK Backend directory exists"
} else {
    Write-Host "  ERROR Backend directory not found"
    $allGood = $false
}

if (Test-Path ".\backend\requirements.txt") {
    Write-Host "  OK requirements.txt exists"
} else {
    Write-Host "  ERROR requirements.txt not found"
    $allGood = $false
}

if (Test-Path ".\frontend\package.json") {
    Write-Host "  OK package.json exists"
} else {
    Write-Host "  ERROR package.json not found"
    $allGood = $false
}

# Check deployment files
Write-Host ""
Write-Host "[4/5] Checking deployment files..."

if (Test-Path ".\render.yaml") {
    Write-Host "  OK render.yaml exists"
} else {
    Write-Host "  WARN render.yaml not found (optional)"
}

if (Test-Path ".\vercel.json") {
    Write-Host "  OK vercel.json exists"
} else {
    Write-Host "  WARN vercel.json not found (optional)"
}

# Check Vercel CLI
Write-Host ""
Write-Host "[5/5] Checking Vercel CLI..."
try {
    $vercelVersion = vercel --version 2>$null
    if ($vercelVersion) {
        Write-Host "  OK Vercel CLI installed: v$vercelVersion"
    } else {
        Write-Host "  WARN Vercel CLI not installed"
        Write-Host "       Install with: npm install -g vercel"
    }
} catch {
    Write-Host "  WARN Vercel CLI not installed"
    Write-Host "       Install with: npm install -g vercel"
}

# Summary
Write-Host ""
Write-Host "========================================"
if ($allGood) {
    Write-Host " SUCCESS: All checks passed!"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "You're ready to deploy!"
    Write-Host ""
    Write-Host "Next steps:"
    Write-Host "  1. Read START_HERE.md"
    Write-Host "  2. Follow DEPLOYMENT_STEPS.md"
    Write-Host ""
} else {
    Write-Host " FAILED: Some checks failed"
    Write-Host "========================================"
    Write-Host ""
    Write-Host "Please install missing requirements above."
}
Write-Host ""

