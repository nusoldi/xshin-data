import json
import pandas as pd
import os

# Function to convert lamports to SOL (1 SOL = 1,000,000,000 lamports)
def lamports_to_sol(lamports_str):
    try:
        return float(lamports_str) / 1_000_000_000
    except (ValueError, TypeError):
        return 0

# Check if the file exists
input_file = 'all_all_validators.json'
if not os.path.exists(input_file):
    print(f"Error: File '{input_file}' not found.")
    exit(1)

# Read the JSON file with explicit encoding
try:
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Successfully loaded {len(data)} validators from {input_file}")
except Exception as e:
    print(f"Error loading JSON file: {e}")
    exit(1)

# Create a list to hold the processed data
processed_data = []

# Extract the relevant data
for i, validator in enumerate(data):
    try:
        pubkey = validator.get('pubkey', '')
        total_score = validator.get('total_score', 0)
        
        # Get validator details
        validator_details = validator.get('validator', {})
        details = validator_details.get('details', {})
        
        # Extract name and other fields
        name = details.get('name', '')
        details_text = details.get('details', '')
        icon_url = details.get('icon_url', '')
        website_url = details.get('website_url', '')
        city = details.get('city', '')
        country = details.get('country', '')
        
        # Get stake details
        stake = details.get('stake', {})
        active = stake.get('active', '0')
        activating = stake.get('activating', '0')
        deactivating = stake.get('deactivating', '0')
        
        # Get target pool stake
        target_pool_stake = details.get('target_pool_stake', '0')
        
        # Get pool stake from validator details
        pool_stake = validator_details.get('pool_stake', {})
        pool_active = pool_stake.get('active', '0')
        pool_activating = pool_stake.get('activating', '0')
        pool_deactivating = pool_stake.get('deactivating', '0')
        
        # Get score details - raw scores
        raw_score = details.get('raw_score', {})
        raw_skip_rate = raw_score.get('skip_rate', 0)
        raw_prior_skip_rate = raw_score.get('prior_skip_rate', 0)
        raw_subsequent_skip_rate = raw_score.get('subsequent_skip_rate', 0)
        raw_cu = raw_score.get('cu', 0)
        raw_latency = raw_score.get('latency', 0)
        raw_llv = raw_score.get('llv', 0)
        raw_cv = raw_score.get('cv', 0)
        raw_vote_inclusion = raw_score.get('vote_inclusion', 0)
        raw_apy = raw_score.get('apy', 0)
        raw_pool_extra_lamports = raw_score.get('pool_extra_lamports', 0)
        raw_city_concentration = raw_score.get('city_concentration', 0)
        raw_country_concentration = raw_score.get('country_concentration', 0)
        
        # Get score details - normalized scores
        normalized_score = details.get('normalized_score', {})
        norm_skip_rate = normalized_score.get('skip_rate', 0)
        norm_prior_skip_rate = normalized_score.get('prior_skip_rate', 0)
        norm_subsequent_skip_rate = normalized_score.get('subsequent_skip_rate', 0)
        norm_cu = normalized_score.get('cu', 0)
        norm_latency = normalized_score.get('latency', 0)
        norm_llv = normalized_score.get('llv', 0)
        norm_cv = normalized_score.get('cv', 0)
        norm_vote_inclusion = normalized_score.get('vote_inclusion', 0)
        norm_apy = normalized_score.get('apy', 0)
        norm_pool_extra_lamports = normalized_score.get('pool_extra_lamports', 0)
        norm_city_concentration = normalized_score.get('city_concentration', 0)
        norm_country_concentration = normalized_score.get('country_concentration', 0)
        
        # Check for noneligibility reasons
        noneligibility_reasons = validator_details.get('noneligibility_reasons', [])
        
        processed_data.append({
            'pubkey': pubkey,
            'total_score': total_score,
            'name': name,
            'details': details_text,
            'icon_url': icon_url,
            'website_url': website_url,
            'city': city,
            'country': country,
            
            # Stake details (will be converted to SOL)
            'active_stake': active,
            'activating_stake': activating,
            'deactivating_stake': deactivating,
            'target_pool_stake': target_pool_stake,
            
            # Pool stake details
            'pool_active_stake': pool_active,
            'pool_activating_stake': pool_activating,
            'pool_deactivating_stake': pool_deactivating,
            
            # Raw scores
            'raw_skip_rate': raw_skip_rate,
            'raw_prior_skip_rate': raw_prior_skip_rate,
            'raw_subsequent_skip_rate': raw_subsequent_skip_rate,
            'raw_cu': raw_cu,
            'raw_latency': raw_latency,
            'raw_llv': raw_llv,
            'raw_cv': raw_cv,
            'raw_vote_inclusion': raw_vote_inclusion,
            'raw_apy': raw_apy,
            'raw_pool_extra_lamports': raw_pool_extra_lamports,
            'raw_city_concentration': raw_city_concentration,
            'raw_country_concentration': raw_country_concentration,
            
            # Normalized scores
            'norm_skip_rate': norm_skip_rate,
            'norm_prior_skip_rate': norm_prior_skip_rate,
            'norm_subsequent_skip_rate': norm_subsequent_skip_rate,
            'norm_cu': norm_cu,
            'norm_latency': norm_latency,
            'norm_llv': norm_llv,
            'norm_cv': norm_cv,
            'norm_vote_inclusion': norm_vote_inclusion,
            'norm_apy': norm_apy,
            'norm_pool_extra_lamports': norm_pool_extra_lamports,
            'norm_city_concentration': norm_city_concentration,
            'norm_country_concentration': norm_country_concentration,
            
            # Other
            'noneligibility_reasons': ', '.join(noneligibility_reasons) if noneligibility_reasons else ''
        })
        
        # Print progress for large files
        if (i + 1) % 1000 == 0:
            print(f"Processed {i + 1} validators...")
            
    except Exception as e:
        print(f"Error processing validator {i}: {e}")

print(f"Total validators processed: {len(processed_data)}")

# Convert to DataFrame
df = pd.DataFrame(processed_data)

# Sort by total_score (descending)
df = df.sort_values(by='total_score', ascending=False).reset_index(drop=True)

# Add rank column (starting from 1)
df.insert(0, 'Rank', range(1, len(df) + 1))

# Convert lamports to SOL for stake fields
stake_columns = [
    'active_stake', 'activating_stake', 'deactivating_stake', 
    'target_pool_stake', 'pool_active_stake', 'pool_activating_stake', 
    'pool_deactivating_stake'
]

for col in stake_columns:
    df[col] = df[col].apply(lamports_to_sol)

# Format the total_score as requested (normalized by 100 with 6 decimals)
df['total_score'] = df['total_score'].apply(lambda x: x * 100)

# Rename columns for better readability
df = df.rename(columns={
    'total_score': 'Total Score',
    'pubkey': 'Pubkey',
    'name': 'Name',
    'details': 'Details',
    'icon_url': 'Icon URL',
    'website_url': 'Website URL',
    'city': 'City',
    'country': 'Country',
    'active_stake': 'Active Stake (SOL)',
    'activating_stake': 'Activating Stake (SOL)',
    'deactivating_stake': 'Deactivating Stake (SOL)',
    'target_pool_stake': 'Target Pool Stake (SOL)',
    'pool_active_stake': 'Pool Active Stake (SOL)',
    'pool_activating_stake': 'Pool Activating Stake (SOL)',
    'pool_deactivating_stake': 'Pool Deactivating Stake (SOL)',
    'raw_skip_rate': 'Skip Rate',
    'raw_prior_skip_rate': 'Prior Skip Rate',
    'raw_subsequent_skip_rate': 'Subsequent Skip Rate',
    'raw_cu': 'CU',
    'raw_latency': 'Latency',
    'raw_llv': 'LLV',
    'raw_cv': 'CV',
    'raw_vote_inclusion': 'Vote Inclusion',
    'raw_apy': 'APY',
    'raw_pool_extra_lamports': 'Pool Extra Lamports',
    'raw_city_concentration': 'City Concentration',
    'raw_country_concentration': 'Country Concentration',
    'norm_skip_rate': 'Normalized Skip Rate',
    'norm_prior_skip_rate': 'Normalized Prior Skip Rate',
    'norm_subsequent_skip_rate': 'Normalized Subsequent Skip Rate',
    'norm_cu': 'Normalized CU',
    'norm_latency': 'Normalized Latency',
    'norm_llv': 'Normalized LLV',
    'norm_cv': 'Normalized CV',
    'norm_vote_inclusion': 'Normalized Vote Inclusion',
    'norm_apy': 'Normalized APY',
    'norm_pool_extra_lamports': 'Normalized Pool Extra Lamports',
    'norm_city_concentration': 'Normalized City Concentration',
    'norm_country_concentration': 'Normalized Country Concentration',
    'noneligibility_reasons': 'Noneligibility Reasons'
})

# Format numeric columns with appropriate precision
df['Total Score'] = df['Total Score'].apply(lambda x: f"{x:.6f}")
df['APY'] = df['APY'].apply(lambda x: f"{x*100:.6f}%")  # Convert to percentage with 6 decimals
df['Skip Rate'] = df['Skip Rate'].apply(lambda x: f"{x*100:.6f}%")  # Convert to percentage with 6 decimals
df['Prior Skip Rate'] = df['Prior Skip Rate'].apply(lambda x: f"{x*100:.6f}%")
df['Subsequent Skip Rate'] = df['Subsequent Skip Rate'].apply(lambda x: f"{x*100:.6f}%")

# Save to Excel
output_file = 'all_validators_rankings.xlsx'
print(f"Saving to Excel file: {output_file}...")
df.to_excel(output_file, index=False)

print(f"Excel file '{output_file}' created successfully with {len(df)} validators ranked by total score.") 