import pandas as pd
from email_validator import validate_email, EmailNotValidError

def parse_companies_file(file_path):
    """
    Parse CSV or Excel file containing company information.
    Expected columns: company_name, email, name (optional), role (optional), designation (optional)
    Returns list of dictionaries with validated and deduplicated data.
    """
    try:
        # Read file based on extension
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(file_path)
        else:
            return []
        
        # Normalize column names (lowercase, strip spaces)
        df.columns = df.columns.str.lower().str.strip()
        
        # Map common column name variations
        column_mapping = {
            'company': 'company_name',
            'company name': 'company_name',
            'organization': 'company_name',
            'email': 'email',
            'email id': 'email',
            'recipient email': 'email',
            'hr email': 'email',
            'contact email': 'email',
            'name': 'name',
            'recipient name': 'name',
            'contact name': 'name',
            'role': 'role',
            'position': 'role',
            'designation': 'designation',
            'title': 'designation',
        }
        
        df.rename(columns=column_mapping, inplace=True)
        
        # Ensure required columns exist
        if 'company_name' not in df.columns or 'email' not in df.columns:
            return []
        
        # Fill optional columns with empty strings
        for col in ['name', 'role', 'designation']:
            if col not in df.columns:
                df[col] = ''
        
        # Remove rows with missing required fields
        df = df.dropna(subset=['company_name', 'email'])
        
        # Remove duplicates based on email
        df = df.drop_duplicates(subset=['email'], keep='first')
        
        # Validate emails and filter
        valid_companies = []
        for _, row in df.iterrows():
            try:
                # Validate email
                validated = validate_email(row['email'])
                
                company_data = {
                    'company_name': str(row['company_name']).strip(),
                    'email': validated.email,
                    'name': str(row.get('name', '')).strip(),
                    'role': str(row.get('role', '')).strip(),
                    'designation': str(row.get('designation', '')).strip(),
                }
                valid_companies.append(company_data)
            except EmailNotValidError:
                # Skip invalid emails
                continue
        
        return valid_companies
    
    except Exception as e:
        print(f"Error parsing file: {e}")
        return []
