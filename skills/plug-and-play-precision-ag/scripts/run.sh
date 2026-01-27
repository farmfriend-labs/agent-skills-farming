#!/bin/bash
# run.sh - Plug-and-Play Precision Agriculture Main Entry Point

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

# Load environment variables
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    print_warning ".env file not found. Using default values."
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# Default values
DEFAULT_GUIDANCE_TYPE="ab_lines"
DEFAULT_SPACING="30"  # feet
DEFAULT_EXPORT_FORMAT="shapefile"

# Function to show help
show_help() {
    cat << EOF
Plug-and-Play Precision Agriculture - Command Line Interface

Usage: ./run.sh [COMMAND] [OPTIONS]

Commands:
  gps-status           Check GPS receiver status and accuracy
  create-field         Create a new field boundary
  list-fields          List all fields
  setup-guidance       Set up guidance lines for a field
  create-prescription  Create variable rate prescription map
  monitor              Monitor real-time field operation
  import-yield         Import yield monitor data
  generate-yield-map   Generate yield map from data
  calculate-roi        Calculate ROI for precision practices
  export-data          Export data in various formats
  backup               Backup all precision data
  import-weather       Import weather data
  test                 Run diagnostic tests
  help                 Show this help message

Options:
  --field-id FIELD     Specify field ID
  --operation-type TYPE Specify operation type (planting, spraying, harvest)
  --format FORMAT      Specify export format (shapefile, geojson, csv)
  --output PATH        Specify output path
  --verbose            Enable verbose output
  --quiet              Suppress output

Examples:
  ./run.sh gps-status
  ./run.sh create-field --name "North Field" --gps-source /dev/ttyUSB0
  ./run.sh setup-guidance --field-id 1 --type ab_lines --spacing 30
  ./run.sh create-prescription --field-id 1 --zones prescription.json
  ./run.sh monitor --field-id 1 --operation-type planting
  ./run.sh calculate-roi --season 2025

For detailed documentation, see SKILL.md
EOF
}

# Function to check GPS status
gps_status() {
    print_info "Checking GPS receiver status..."

    if [ -z "$GPS_PORT" ]; then
        print_error "GPS_PORT not configured in .env"
        exit 1
    fi

    if [ ! -e "$GPS_PORT" ]; then
        print_error "GPS device not found: $GPS_PORT"
        exit 1
    fi

    python3 scripts/gps_status.py --port "$GPS_PORT" --baudrate "${GPS_BAUDRATE:-9600}"
}

# Function to create field
create_field() {
    print_info "Creating new field boundary..."

    FIELD_NAME=""
    GPS_SOURCE=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --name)
                FIELD_NAME="$2"
                shift 2
                ;;
            --gps-source)
                GPS_SOURCE="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    if [ -z "$FIELD_NAME" ]; then
        print_error "Field name required (--name)"
        exit 1
    fi

    python3 scripts/field_manager.py create --name "$FIELD_NAME" --gps-source "${GPS_SOURCE:-$GPS_PORT}"
}

# Function to list fields
list_fields() {
    print_info "Listing all fields..."
    python3 scripts/field_manager.py list
}

# Function to setup guidance
setup_guidance() {
    print_info "Setting up guidance lines..."

    FIELD_ID=""
    GUIDANCE_TYPE="$DEFAULT_GUIDANCE_TYPE"
    SPACING="$DEFAULT_SPACING"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --field-id)
                FIELD_ID="$2"
                shift 2
                ;;
            --type)
                GUIDANCE_TYPE="$2"
                shift 2
                ;;
            --spacing)
                SPACING="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    if [ -z "$FIELD_ID" ]; then
        print_error "Field ID required (--field-id)"
        exit 1
    fi

    python3 scripts/guidance.py setup --field-id "$FIELD_ID" --type "$GUIDANCE_TYPE" --spacing "$SPACING"
}

# Function to create prescription
create_prescription() {
    print_info "Creating variable rate prescription map..."

    FIELD_ID=""
    ZONES_FILE=""
    INPUT_TYPE="fertilizer"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --field-id)
                FIELD_ID="$2"
                shift 2
                ;;
            --zones)
                ZONES_FILE="$2"
                shift 2
                ;;
            --input-type)
                INPUT_TYPE="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    if [ -z "$FIELD_ID" ] || [ -z "$ZONES_FILE" ]; then
        print_error "Field ID and zones file required"
        exit 1
    fi

    python3 scripts/prescription.py create --field-id "$FIELD_ID" --zones "$ZONES_FILE" --input-type "$INPUT_TYPE"
}

# Function to monitor operation
monitor_operation() {
    print_info "Starting operation monitor..."

    FIELD_ID=""
    OPERATION_TYPE=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --field-id)
                FIELD_ID="$2"
                shift 2
                ;;
            --operation-type)
                OPERATION_TYPE="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    if [ -z "$FIELD_ID" ]; then
        print_error "Field ID required (--field-id)"
        exit 1
    fi

    python3 scripts/monitor.py --field-id "$FIELD_ID" --operation-type "${OPERATION_TYPE}"
}

# Function to import yield data
import_yield() {
    print_info "Importing yield data..."

    INPUT_FILE=""
    FIELD_ID=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --file)
                INPUT_FILE="$2"
                shift 2
                ;;
            --field-id)
                FIELD_ID="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    if [ -z "$INPUT_FILE" ]; then
        print_error "Input file required (--file)"
        exit 1
    fi

    python3 scripts/yield_processor.py import --file "$INPUT_FILE" --field-id "${FIELD_ID}"
}

# Function to generate yield map
generate_yield_map() {
    print_info "Generating yield map..."

    FIELD_ID=""
    OUTPUT_FORMAT="$DEFAULT_EXPORT_FORMAT"

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --field-id)
                FIELD_ID="$2"
                shift 2
                ;;
            --format)
                OUTPUT_FORMAT="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    if [ -z "$FIELD_ID" ]; then
        print_error "Field ID required (--field-id)"
        exit 1
    fi

    python3 scripts/yield_map.py generate --field-id "$FIELD_ID" --format "$OUTPUT_FORMAT"
}

# Function to calculate ROI
calculate_roi() {
    print_info "Calculating ROI..."

    SEASON=""
    FIELDS=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --season)
                SEASON="$2"
                shift 2
                ;;
            --fields)
                FIELDS="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    python3 scripts/roi_calculator.py --season "${SEASON:-$(date +%Y)}" --fields "${FIELDS:-all}"
}

# Function to export data
export_data() {
    print_info "Exporting data..."

    DATA_TYPE=""
    FORMAT="$DEFAULT_EXPORT_FORMAT"
    OUTPUT_PATH=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --data-type)
                DATA_TYPE="$2"
                shift 2
                ;;
            --format)
                FORMAT="$2"
                shift 2
                ;;
            --output)
                OUTPUT_PATH="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    if [ -z "$DATA_TYPE" ]; then
        print_error "Data type required (--data-type)"
        exit 1
    fi

    python3 scripts/data_export.py --data-type "$DATA_TYPE" --format "$FORMAT" --output "${OUTPUT_PATH}"
}

# Function to backup data
backup_data() {
    print_info "Creating backup..."

    BACKUP_LOCATION="${BACKUP_PATH:-/var/backups/precision-ag}"

    python3 scripts/backup.py --location "$BACKUP_LOCATION"
}

# Function to import weather
import_weather() {
    print_info "Importing weather data..."

    START_DATE=""
    END_DATE=""

    # Parse arguments
    while [[ $# -gt 0 ]]; do
        case $1 in
            --start-date)
                START_DATE="$2"
                shift 2
                ;;
            --end-date)
                END_DATE="$2"
                shift 2
                ;;
            *)
                shift
                ;;
        esac
    done

    python3 scripts/weather.py import --start-date "${START_DATE}" --end-date "${END_DATE}"
}

# Function to run tests
run_tests() {
    print_info "Running diagnostic tests..."

    bash scripts/test.sh
}

# Main script logic
COMMAND="${1:-help}"

shift

case "$COMMAND" in
    gps-status)
        gps_status "$@"
        ;;
    create-field)
        create_field "$@"
        ;;
    list-fields)
        list_fields "$@"
        ;;
    setup-guidance)
        setup_guidance "$@"
        ;;
    create-prescription)
        create_prescription "$@"
        ;;
    monitor)
        monitor_operation "$@"
        ;;
    import-yield)
        import_yield "$@"
        ;;
    generate-yield-map)
        generate_yield_map "$@"
        ;;
    calculate-roi)
        calculate_roi "$@"
        ;;
    export-data)
        export_data "$@"
        ;;
    backup)
        backup_data "$@"
        ;;
    import-weather)
        import_weather "$@"
        ;;
    test)
        run_tests "$@"
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Unknown command: $COMMAND"
        echo ""
        show_help
        exit 1
        ;;
esac
