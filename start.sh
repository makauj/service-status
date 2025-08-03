#!/bin/bash

# Collection Management System Startup Script

set -e

echo "🚀 Collection Management System"
echo "================================"

# Function to check if Docker is running
check_docker() {
    if ! sudo docker info > /dev/null 2>&1; then
        echo "❌ Docker is not running. Please start Docker and try again."
        exit 1
    fi
}

# Function to check if Docker Compose is available
check_docker_compose() {
    if ! command -v docker compose &> /dev/null; then
        echo "❌ Docker Compose is not installed. Please install it and try again."
        exit 1
    fi
}

# Function to start the application
start_app() {
    echo "📦 Starting Collection Management System..."
    echo "⏳ This may take a few minutes on first run..."
    
    sudo docker compose up --build -d
    
    echo "✅ Application started successfully!"
    echo ""
    echo "🌐 Access the application:"
    echo "   • Frontend: http://localhost:3000"
    echo "   • API Docs: http://localhost:8000/docs"
    echo "   • Health Check: http://localhost:8000/health"
    echo ""
    echo "📊 To view logs: ./start.sh logs"
    echo "🛑 To stop: ./start.sh stop"
}

# Function to stop the application
stop_app() {
    echo "🛑 Stopping Collection Management System..."
    sudo docker compose down
    echo "✅ Application stopped."
}

# Function to view logs
show_logs() {
    echo "📋 Application logs:"
    sudo docker compose logs -f
}

# Function to restart the application
restart_app() {
    echo "🔄 Restarting Collection Management System..."
    sudo docker compose down
    sudo docker compose up --build -d
    echo "✅ Application restarted!"
}

# Function to create sample data
create_sample_data() {
    echo "📊 Creating sample Excel file..."
    python3 sample_data.py
    echo "✅ Sample data created: sample_collections.xlsx"
    echo "📤 You can now upload this file through the web interface!"
}

# Function to show status
show_status() {
    echo "📊 Application Status:"
    sudo docker compose ps
    echo ""
    echo "🔗 URLs:"
    echo "   • Frontend: http://localhost:3000"
    echo "   • API: http://localhost:8000"
    echo "   • Database: localhost:5432"
}

# Function to show help
show_help() {
    echo "Usage: ./start.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  start     Start the application (default)"
    echo "  stop      Stop the application"
    echo "  restart   Restart the application"
    echo "  logs      Show application logs"
    echo "  status    Show application status"
    echo "  sample    Create sample Excel data"
    echo "  help      Show this help message"
    echo ""
    echo "Examples:"
    echo "  ./start.sh start"
    echo "  ./start.sh logs"
    echo "  ./start.sh stop"
}

# Main script logic
case "${1:-start}" in
    "start")
        check_docker
        check_docker_compose
        start_app
        ;;
    "stop")
        check_docker
        check_docker_compose
        stop_app
        ;;
    "restart")
        check_docker
        check_docker_compose
        restart_app
        ;;
    "logs")
        check_docker
        check_docker_compose
        show_logs
        ;;
    "status")
        check_docker
        check_docker_compose
        show_status
        ;;
    "sample")
        create_sample_data
        ;;
    "help"|"-h"|"--help")
        show_help
        ;;
    *)
        echo "❌ Unknown command: $1"
        echo "Use './start.sh help' for usage information."
        exit 1
        ;;
esac 