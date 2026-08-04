def export_user_data(user_id):
    user = get_user(user_id)
    # No DLP
    requests.post("https://external.com/api", json=user)
    return True

def backup_to_cloud():
    # Unencrypted backup
    data = get_all_sensitive_data()
    with open("/backup/plaintext.json", "w") as f:
        json.dump(data, f)
    requests.post("https://cloud-storage.com/upload", files={"file": open("/backup/plaintext.json")})