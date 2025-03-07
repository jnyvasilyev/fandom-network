# Fandom Character Network

This project creates an interactive network visualization of character relationships from any Fandom wiki, based on mentions in character history sections.

## Features

- Builds character networks based on history section mentions
- Interactive visualization with character images
- Node sizes reflect character importance
- Edge weights show strength of relationships
- Hover for detailed character statistics
- Caches API responses for faster subsequent runs

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd fandom-network
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

Run the script with a Fandom wiki domain:

```bash
python main.py <wiki_domain>
```

For example:
```bash
python main.py harrypotter
```

### Options

- `--cache-dir`: Specify a custom cache directory (default: `.cache`)
- `--clear-cache`: Clear the cache before starting

## How it Works

1. The script fetches all character pages from the specified wiki
2. For each character:
   - Retrieves their history section
   - Counts mentions of other characters
   - Creates weighted edges based on mention counts
3. Creates an interactive visualization where:
   - Node size = sqrt(number_of_connections * sum_of_weights)
   - Edge width = normalized mention count
   - Character images are displayed as nodes (when available)
   - Hover over nodes for detailed statistics

## Project Structure

```
fandom_network/
├── src/
│   ├── api/           # Wiki API interaction
│   ├── network/       # Network building and analysis
│   ├── visualization/ # Interactive visualization
│   └── utils/         # Utility functions
├── main.py           # Main script
└── requirements.txt  # Dependencies
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details. 