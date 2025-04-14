import streamlit as st
import zxcvbn
import re

def check_password_strength(password):
    if not password:
        return {
            'strength': 0,
            'score': 0,
            'feedback': []
        }
    
    result = zxcvbn.zxcvbn(password)
    score = result['score'] / 4  # Normalize score to 0-1
    feedback = []
    
    # Length check
    if len(password) < 8:
        feedback.append("Password is too short (minimum 8 characters)")
    elif len(password) >= 12:
        feedback.append("Good password length")
    
    # Complexity checks
    if not re.search(r'[A-Z]', password):
        feedback.append("Add uppercase letters")
    if not re.search(r'[a-z]', password):
        feedback.append("Add lowercase letters")
    if not re.search(r'[0-9]', password):
        feedback.append("Add numbers")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        feedback.append("Add special characters")
    
    # Strength level
    if score < 0.3:
        strength = "Weak"
    elif score < 0.6:
        strength = "Medium"
    elif score < 0.8:
        strength = "Strong"
    else:
        strength = "Very Strong"
    
    return {
        'strength': strength,
        'score': score,
        'feedback': feedback
    }

def main():
    st.set_page_config(
        page_title="Password Strength Meter",
        page_icon="🔒",
        layout="centered"
    )
    
    st.title("🔒 Password Strength Meter")
    st.markdown("Check the strength of your password and get suggestions for improvement.")
    
    password = st.text_input(
        "Enter your password",
        type="password",
        placeholder="Type your password here..."
    )
    
    if password:
        result = check_password_strength(password)
        
        # Display strength meter
        st.progress(result['score'])
        
        # Display strength level with color
        if result['strength'] == "Weak":
            st.error(f"Strength: {result['strength']}")
        elif result['strength'] == "Medium":
            st.warning(f"Strength: {result['strength']}")
        else:
            st.success(f"Strength: {result['strength']}")
        
        # Display feedback
        st.subheader("Suggestions:")
        for suggestion in result['feedback']:
            st.write(f"- {suggestion}")
        
        # Display score
        st.metric("Password Score", f"{result['score']:.2%}")
    
    # Add some helpful tips
    st.markdown("""
    ### Tips for a strong password:
    - Use at least 12 characters
    - Include uppercase and lowercase letters
    - Add numbers and special characters
    - Avoid common words and patterns
    - Don't use personal information
    """)

if __name__ == "__main__":
    main() 