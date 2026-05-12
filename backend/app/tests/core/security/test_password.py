from app.core.security.password import verify_password, get_password_hash

def test_verify_password_correct():
    password = "SuperSecretPassword123!"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True

def test_verify_password_incorrect():
    password = "SuperSecretPassword123!"
    incorrect_password = "WrongPassword456!"
    hashed = get_password_hash(password)
    assert verify_password(incorrect_password, hashed) is False

def test_verify_password_long_password_truncation():
    # Passwords longer than 72 bytes are truncated to 72 bytes by bcrypt logic in this app
    long_password = "a" * 100
    # The hash should be based on the first 72 characters
    hashed = get_password_hash(long_password)

    # Testing that it verifies successfully against the exact long password
    assert verify_password(long_password, hashed) is True

    # Testing that it also verifies successfully if only the first 72 characters match
    # Since the system silently truncates to 72 chars, another 100 char string with the same 72 prefix matches
    another_long_password = ("a" * 72) + ("b" * 28)
    assert verify_password(another_long_password, hashed) is True
