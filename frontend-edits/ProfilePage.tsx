//B/E = backend edit

// Note: This file is part of backend integration edits.
// Replace this in `redback-fit-web/src/routes/ProfilePage/ProfilePage.tsx` in the frontend repo.
// Requires backend API endpoints to function correctly. Remove triple quoted comments in /api/routes.py 
import React, { useState, useEffect } from 'react'; //B/E added useEffect
import styles from './ProfilePage.module.css';

const ProfilePage: React.FC = () => {
	const [userData, setUserData] = useState({
		name: 'Austin Blaze',
		account: 'redback.operations@deakin.edu.au',
		birthDate: '2000-01-01',
		gender: 'Male',
	});
	const [avatar, setAvatar] = useState('src/assets/ProfilePic.png'); // Default avatar path

	// B/E Fetch profile data when the component mounts
	useEffect(() => {
		const fetchProfile = async () => {
			try {
				const response = await fetch('http://localhost:5000/api/profile');
				if (response.ok) {
					const data = await response.json();
					setUserData({
						name: data.name,
						account: data.account,
						birthDate: data.birthDate,
						gender: data.gender,
					});
					setAvatar(data.avatar || 'src/assets/ProfilePic.png');
				} else {
					console.error('Failed to fetch profile data');
				}
			} catch (error) {
				console.error('Error fetching profile data:', error);
			}
		};
		fetchProfile();
	}, []); // Empty dependency array means this runs once when the component mounts
	////////////////////////////////////////////////////////////////////////////////

	const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		const { name, value } = e.target;
		setUserData({ ...userData, [name]: value });
	};

	const handleGenderChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
		setUserData({ ...userData, gender: e.target.value });
	};

	const handleAvatarChange = (e: React.ChangeEvent<HTMLInputElement>) => {
		if (e.target.files && e.target.files[0]) {
			const file = e.target.files[0];
			const newAvatarUrl = URL.createObjectURL(file);
			setAvatar(newAvatarUrl);
		}
	};

	// B/E edit handleSave
	const handleSave = async () => {
		try {
			const response = await fetch('http://localhost:5000/api/profile', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({
					name: userData.name,
					account: userData.account,
					birthDate: userData.birthDate,
					gender: userData.gender,
					avatar: avatar,
				}),
			});

			if (response.ok) {
				alert('Profile saved successfully!');
			} else {
				console.error('Failed to save profile');
				alert('Error saving profile');
			}
		} catch (error) {
			console.error('Error saving profile:', error);
			alert('Error saving profile');
		}
	};

	const handleBack = () => {
		window.history.back();
	};

	return (
		<div className={styles.profilePageContainer}>
			<button className={styles.backButton} onClick={handleBack}>
				Back
			</button>
			<div className={styles.formContainer}>
				<div className={styles.avatarSection}>
					<img src={avatar} alt="User Avatar" className={styles.avatar} />
					<label htmlFor="avatarUpload" className={styles.uploadButton}>
						Change Avatar
					</label>
					<input
						id="avatarUpload"
						type="file"
						accept="image/*"
						className={styles.uploadInput}
						onChange={handleAvatarChange}
					/>
				</div>
				<div className={styles.formGroup}>
					<label className={styles.formLabel}>Name</label>
					<input
						type="text"
						name="name"
						value={userData.name}
						onChange={handleInputChange}
						className={styles.formInput}
					/>
				</div>
				<div className={styles.formGroup}>
					<label className={styles.formLabel}>Account</label>
					<input
						type="email"
						name="account"
						value={userData.account}
						onChange={handleInputChange}
						className={styles.formInput}
					/>
				</div>
				<div className={styles.formGroup}>
					<label className={styles.formLabel}>Birth Date</label>
					<input
						type="date"
						name="birthDate"
						value={userData.birthDate}
						onChange={handleInputChange}
						className={styles.formInput}
					/>
				</div>
				<div className={styles.formGroup}>
					<label className={styles.formLabel}>Gender</label>
					<select
						name="gender"
						value={userData.gender}
						onChange={handleGenderChange}
						className={styles.formSelect}
					>
						<option value="Male">Male</option>
						<option value="Female">Female</option>
						<option value="Other">Other</option>
					</select>
				</div>
				<button className={styles.saveButton} onClick={handleSave}>
					Save
				</button>
			</div>
		</div>
	);
};

export default ProfilePage;
