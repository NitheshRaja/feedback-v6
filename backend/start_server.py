"""
Startup script for the backend server
"""
import uvicorn
import sys

if __name__ == "__main__":
    try:
        print("Starting L1 Feedback Sentiment Analysis API...")
        print("Server will be available at: http://localhost:8000")
        print("API Documentation: http://localhost:8000/docs")
        print("\nPress CTRL+C to stop the server\n")
        
        uvicorn.run(
            "app.main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info"
        )
    except KeyboardInterrupt:
        print("\n\nServer stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error starting server: {e}")
        print("\nTroubleshooting:")
        print("1. Check if PostgreSQL is running")
        print("2. Verify DATABASE_URL in .env file")
        print("3. Ensure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)




