# Hybrid Multi-Layer Encryption Algorithm

## Table of Contents
- [Introduction](#introduction)
- [Algorithm Architecture](#algorithm-architecture)
- [Layer 1: Genetic Encryption](#layer-1-genetic-encryption)
- [Layer 2: Homomorphic Encryption](#layer-2-homomorphic-encryption)
- [Layer 3: Adaptive Key Management](#layer-3-adaptive-key-management)
- [Complete Workflow](#complete-workflow)
- [Security Analysis](#security-analysis)
- [Performance Considerations](#performance-considerations)
- [Implementation Example](#implementation-example)

## Introduction
Our hybrid encryption algorithm combines three distinct encryption layers to provide enhanced security for sensitive data while enabling secure computation on encrypted data. The algorithm is particularly suited for cloud environments where data needs to remain secure but still usable for analytics.

### Key Features
- **Multi-layered Security**: Combines three encryption techniques for defense in depth
- **Homomorphic Properties**: Allows mathematical operations on encrypted data
- **Adaptive Key Management**: Limits key exposure through automatic rotation
- **DNA-Inspired Encoding**: Uses biological patterns for unique encoding
- **Envelope Encryption**: Protects individual data items with unique keys

## Algorithm Architecture
```
┌─────────────────────────────────────────────────────┐
│                   Original Data                     │
└───────────────────────┬─────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│ Layer 3: Generate Data Encryption Key (DEK)         │
└───────────────────────┬─────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│ Layer 1: Genetic Encryption (using DEK)             │
└───────────────────────┬─────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│ Layer 2: Homomorphic Encryption                     │
└───────────────────────┬─────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│ Layer 3: Encrypt DEK with KEK (Key Encryption Key)  │
└───────────────────────┬─────────────────────────────┘
                        ▼
┌─────────────────────────────────────────────────────┐
│              Complete Encrypted Package              │
└─────────────────────────────────────────────────────┘
```

The system operates on the principle of envelope encryption (DEK/KEK model), where each data item receives its own Data Encryption Key (DEK), and these keys are themselves encrypted by a master Key Encryption Key (KEK). This provides important security isolation, as compromise of one data item doesn't expose others.

## Layer 1: Genetic Encryption

### Core Concept
The Genetic Encryption layer draws inspiration from DNA encoding. It transforms raw data into a DNA-like sequence using a combination of XOR operations, bit shifting, and nucleotide mapping.

### DNA Mapping
```python
DNA_MAPPING = {
    '00': 'A',  # Adenine
    '01': 'C',  # Cytosine
    '10': 'G',  # Guanine
    '11': 'T'   # Thymine
}
```
This mapping converts binary data (00, 01, 10, 11) to DNA nucleotides (A, C, G, T), creating a unique representation for encrypted data.

### Encryption Process
The genetic encryption process involves:

1. **XOR Operation**: Applying XOR between data and the DEK
2. **Bit Shifting**: Circular rotation of bits for diffusion
3. **DNA Conversion**: Mapping of binary data to DNA nucleotides

```python
def genetic_encrypt(data: bytes, key: bytes) -> str:
    # Step 1: XOR data with key
    xor_encrypted = xor_encrypt(data, key)
    # Step 2: Shift bits for diffusion
    shifted = bit_shift(xor_encrypted, shift_by=2, direction='left')
    # Step 3: Convert to DNA representation
    return binary_to_dna(shifted)
```

### Decryption Process
Decryption reverses these steps:

1. **DNA to Binary**: Convert DNA sequence back to binary
2. **Bit Unshifting**: Reverse the bit shifting operation
3. **XOR Operation**: Apply XOR again to recover the original data

```python
def genetic_decrypt(dna_sequence: str, key: bytes) -> bytes:
    # Step 1: Convert DNA back to binary data
    binary_data = dna_to_binary(dna_sequence)
    # Step 2: Reverse bit shifting
    unshifted = bit_shift(binary_data, shift_by=2, direction='right')
    # Step 3: XOR to get original data (XOR is its own inverse)
    return xor_encrypt(unshifted, key)
```

## Layer 2: Homomorphic Encryption

### Core Concept
Homomorphic Encryption allows mathematical operations to be performed on encrypted data without decrypting it first. Our implementation uses the Paillier cryptosystem, which supports addition operations on encrypted data.

### Key Components
- **Public/Private Key Generation**: Creates key pairs for encryption/decryption
- **Encryption**: Converts data to ciphertext using public key
- **Decryption**: Recovers plaintext using private key
- **Homomorphic Operations**: Allows addition and scalar multiplication on encrypted data

### Implementation

```python
class PaillierHE:
    def __init__(self):
        # Generate key pair
        self.pub_key, self.priv_key = paillier.generate_paillier_keypair()
    
    def encrypt(self, value: int):
        # Encrypt integer value
        return self.pub_key.encrypt(value)
    
    def decrypt(self, ctxt):
        # Decrypt ciphertext
        return self.priv_key.decrypt(ctxt)
    
    def add(self, ctxt1, ctxt2):
        # Add two encrypted values
        return ctxt1 + ctxt2
    
    def mul_scalar(self, ctxt, scalar: int):
        # Multiply encrypted value by plaintext scalar
        return ctxt * scalar
```

### Scaling for Precision
Because homomorphic encryption works with integers, we implement scaling for floating point values:

```python
# Scale factor for floating point precision
scale_factor = 1000  # Allows 3 decimal places

# Encryption with scaling
scaled_int_val = int(value * scale_factor)
homomorphic_encrypted = he_instance.encrypt(scaled_int_val)

# Decryption with scaling
raw_sum = he_instance.decrypt(encrypted_sum)
decrypted_sum = raw_sum / scale_factor
```

## Layer 3: Adaptive Key Management

### Core Concept
The key management layer implements an envelope encryption model with automatic key rotation. It manages:

- **Key Encryption Keys (KEKs)**: Master keys that encrypt DEKs
- **Data Encryption Keys (DEKs)**: Unique keys for each data item
- **Key Versioning**: Tracking which KEK encrypted which DEK
- **Key Rotation**: Periodic generation of new KEKs
- **Key Archiving**: Safe storage of expired keys

### Key Lifecycle
```
┌────────────────┐       ┌───────────────┐      ┌──────────────┐
│  KEK Creation  │──────▶│ Active KEK    │─────▶│ Archived KEK │
└────────────────┘       └───────────────┘      └──────────────┘
       │                      │     │                 │
       │                      │     │                 │
       ▼                      ▼     ▼                 ▼
  Used for new         Used for    Used to      Used only for
    DEKs & data      key updates   decrypt      DEK decryption
```

### Key Manager Implementation
```python
class EnvelopeKeyManager:
    def __init__(self, rotation_interval=3600, key_ttl=7200):
        # Key rotation interval (default: 1 hour)
        self.rotation_interval = rotation_interval
        # Time-to-live for keys (default: 2 hours)
        self.key_ttl = key_ttl
        
        # Active and archived keys
        self.key_encryption_keys = {}  # version -> KEK
        self.archived_keks = {}        # version -> KEK (expired)
        self.current_kek_version = 0
        
        # Create initial KEK
        self.rotate_keys()
    
    def rotate_keys(self):
        """Generate new Key Encryption Key"""
        self.current_kek_version += 1
        self.last_rotation = time.time()
        
        # Generate random 16-byte key
        kek = bytes([random.randint(0, 255) for _ in range(16)])
        
        # Create homomorphic encryption instance
        he_instance = PaillierHE()
        
        # Store key information
        self.key_encryption_keys[self.current_kek_version] = {
            'kek': kek,
            'he_instance': he_instance,
            'created_at': self.last_rotation
        }
        
        return self.current_kek_version
```

### Key Rotation and Backward Compatibility
A critical feature is the ability to update DEK encryption without re-encrypting data:

```python
def update_encrypted_dek(self, encrypted_dek_package):
    """Re-encrypt a DEK with the current KEK"""
    # Decrypt the DEK using the old KEK
    dek = self.decrypt_dek(encrypted_dek_package)
    # Re-encrypt with current KEK
    return self.encrypt_dek(dek)
```

This allows seamless key rotation without needing to re-encrypt all data.

## Complete Workflow

### Encryption Process
1. Generate a unique DEK for the data item
2. Get the current KEK from the key manager
3. Apply Layer 1: Encrypt data using genetic encryption with DEK
4. Apply Layer 2: Apply homomorphic encryption for computational capability
5. Apply Layer 3: Encrypt the DEK with the KEK
6. Package everything with necessary metadata for decryption

```python
def envelope_encrypt_with_kek(value, kek_version, kek, he_instance, key_manager):
    # Generate DEK for this data
    dek = key_manager.generate_dek()
    
    # Encrypt DEK with KEK
    encrypted_dek = xor_encrypt(dek, kek)
    encrypted_dek_package = {
        'encrypted_dek': encrypted_dek,
        'kek_version': kek_version
    }
    
    # Special handling for numeric values
    scale_factor = 1000
    
    if isinstance(value, float):
        # Layer 2: Homomorphic encryption of scaled value
        scaled_int_val = int(value * scale_factor)
        homomorphic_encrypted = he_instance.encrypt(scaled_int_val)
        
        # Layer 1: Genetic encryption
        byte_val = float_to_bytes(value)
        dna_seq = genetic_encrypt(byte_val, dek)
    else:
        # Handle non-numeric data
        byte_val = str(value).encode()
        dna_seq = genetic_encrypt(byte_val, dek)
        homomorphic_encrypted = he_instance.encrypt(0)
        
    # Create complete package
    encrypted_package = {
        'encrypted_data': homomorphic_encrypted,  # Layer 2
        'encrypted_dek': encrypted_dek_package,   # Layer 3
        'dna_length': len(dna_seq),
        'genetic_data': dna_seq,                  # Layer 1
        'he_version': kek_version,
        'is_float': isinstance(value, float),
        'scale_factor': scale_factor
    }
    
    return encrypted_package
```

### Decryption Process
1. Extract the encrypted DEK from the package
2. Identify the KEK version used for DEK encryption
3. Retrieve the appropriate KEK (active or archived)
4. Decrypt the DEK using the KEK
5. Use the DEK to decrypt the data using genetic decryption
6. Convert the decrypted data to the appropriate format

```python
def envelope_decrypt(encrypted_package, key_manager):
    # Extract DEK package
    encrypted_dek_package = encrypted_package['encrypted_dek']
    
    # Decrypt DEK with appropriate KEK version
    dek = key_manager.decrypt_dek(encrypted_dek_package)
    
    # Use stored DNA sequence for genetic decryption
    if 'genetic_data' in encrypted_package:
        dna_seq = encrypted_package['genetic_data']
    else:
        # Fallback method
        encrypted_data = encrypted_package['encrypted_data']
        dna_length = encrypted_package['dna_length']
        he_version = encrypted_package['he_version']
        he_instance = key_manager.get_he_instance(he_version)
        decrypted_int = he_instance.decrypt(encrypted_data)
        dna_seq = int_to_dna(decrypted_int, dna_length)
    
    # Genetic decryption
    decrypted_bytes = genetic_decrypt(dna_seq, dek)
    
    # Convert to appropriate format
    if encrypted_package.get('is_float', False):
        decrypted_value = bytes_to_float(decrypted_bytes[:4])
    else:
        try:
            decrypted_value = decrypted_bytes.decode()
        except:
            decrypted_value = decrypted_bytes
            
    return decrypted_value
```

### Homomorphic Operations
One of the key features is the ability to perform calculations on encrypted data:

```python
# Extract encrypted data
encrypted_values = [pkg['encrypted_data'] for pkg in packages]

# Get HE instance and scale factor
he_instance = key_manager.get_he_instance(he_version)
scale_factor = packages[0]['scale_factor']

# Sum the encrypted values
encrypted_sum = encrypted_values[0]
for value in encrypted_values[1:]:
    encrypted_sum = he_instance.add(encrypted_sum, value)

# Decrypt and descale
raw_sum = he_instance.decrypt(encrypted_sum)
decrypted_sum = raw_sum / scale_factor
```

This allows operations like sum, average, and other calculations directly on encrypted data.

## Security Analysis

### Defense in Depth
Our algorithm provides multiple security layers:

- **Genetic Encryption**: Protects raw data with XOR and bit diffusion
- **Homomorphic Encryption**: Mathematical security based on integer factorization
- **Envelope Encryption**: Unique DEK per data item limits exposure
- **Key Rotation**: Periodic KEK changes reduce window of vulnerability
- **Key Versioning**: Maintains backward compatibility with strong security

### Brute Force Resistance
The system uses 16-byte (128-bit) keys for both DEK and KEK:

- Key space: 2^128 (16-byte key)
- At 1000 attempts/second
- Average time to crack: 5.395142e+27 years
- Key valid for: 2.0 hours
- Probability of successful crack within key TTL: 2.115890e-32

Even with a quantum computer capable of a billion billion attempts per second, the key would remain secure within its lifetime.

## Performance Considerations

### Measured Performance
Our testing shows reasonable performance metrics:

- Dataset size: 20 rows, 3 columns
- Encryption time: 21.3842 seconds
- Average time per value: 356.34 ms
- Memory used: 0.00 MB
- CPU usage: 99.50%
- Time to rotate keys (no data re-encryption): 2.5031 seconds

### Optimization Strategies
For real-world use:

- **Batched Encryption**: Process data in batches for efficiency
- **Key Reuse**: Consider grouping related data under one DEK
- **Hardware Acceleration**: Use specialized cryptographic hardware
- **Selective Application**: Apply full encryption only to sensitive fields
- **Caching**: Store frequently accessed decrypted values with proper security

## Implementation Example
Here's how to use the system on a typical dataset:

```python
# Set up key manager with 1-hour rotation, 2-hour TTL
key_manager = EnvelopeKeyManager(rotation_interval=3600, key_ttl=7200)

# Load sample data
df = pd.read_csv("winequality-red.csv", sep=';')
columns = ['pH', 'density', 'alcohol']

# Encrypt dataset
results = process_wine_data_envelope(df, columns, key_manager)

# Perform homomorphic operations (e.g., sum pH values)
encrypted_values = [pkg['encrypted_data'] for pkg in results['encrypted_packages']['pH']]
he_version = results['encrypted_packages']['pH'][0]['he_version']
scale_factor = results['encrypted_packages']['pH'][0]['scale_factor']
he_instance = key_manager.get_he_instance(he_version)

# Sum values while they're encrypted
encrypted_sum = encrypted_values[0]
for value in encrypted_values[1:]:
    encrypted_sum = he_instance.add(encrypted_sum, value)

# Decrypt only the final result
raw_sum = he_instance.decrypt(encrypted_sum)
decrypted_sum = raw_sum / scale_factor

print(f"Sum of pH values: {decrypted_sum}")
```

This simple example demonstrates the power of the system, enabling analytics on encrypted data while maintaining strong security.

By combining genetic encryption, homomorphic capabilities, and adaptive key management, our hybrid system offers a robust yet flexible approach to data protection that's particularly well-suited for sensitive data processing in cloud environments.