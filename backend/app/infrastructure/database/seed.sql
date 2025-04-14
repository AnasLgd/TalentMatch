-- ---------------------
-- SEED TalentMatch - Version stable
-- ---------------------

-- ⚡ Suppression des données existantes (order-safe)
DELETE FROM consultant_skills;
DELETE FROM consultants;
DELETE FROM users;
DELETE FROM tender_skills;
DELETE FROM tenders;
DELETE FROM skills;
DELETE FROM companies;

-- 1️⃣ Companies
INSERT INTO companies (id, name, description, website, address, is_esn, created_at)
VALUES
(1, 'TechWave ESN', 'Entreprise de Services du Numérique spécialisée en transformation digitale.', 'https://www.techwave.com', '10 rue de l''Innovation, Paris', TRUE, NOW())
ON CONFLICT (id) DO NOTHING;

-- 2️⃣ Users
INSERT INTO users (id, email, password_hash, full_name, role, company_id, is_active, created_at)
VALUES
(1, 'alice@techwave.com', '$2b$12$dummyhash', 'Alice Dupont', 'ADMIN', 1, TRUE, NOW()),
(2, 'bruno@techwave.com', '$2b$12$dummyhash', 'Bruno Martin', 'MANAGER', 1, TRUE, NOW()),
(3, 'carla@techwave.com', '$2b$12$dummyhash', 'Carla Morel', 'CONSULTANT', 1, TRUE, NOW()),
(4, 'daniel@techwave.com', '$2b$12$dummyhash', 'Daniel Leroy', 'CONSULTANT', 1, TRUE, NOW()),
(5, 'emma@techwave.com', '$2b$12$dummyhash', 'Emma Lemoine', 'CONSULTANT', 1, TRUE, NOW())
ON CONFLICT (id) DO NOTHING;

-- 3️⃣ Skills
INSERT INTO skills (id, name, category, description, created_at)
VALUES
(1, 'React', 'framework', 'Librairie JS pour construire des interfaces', NOW()),
(2, 'Python', 'programming_language', 'Langage de programmation polyvalent', NOW()),
(3, 'AWS', 'cloud', 'Services cloud d''Amazon', NOW()),
(4, 'Docker', 'devops', 'Conteneurisation d''applications', NOW()),
(5, 'PostgreSQL', 'database', 'Système de gestion de base de données relationnelle', NOW()),
(6, 'Scrum', 'methodology', 'Méthodologie Agile', NOW()),
(7, 'Figma', 'other', 'Outil de design UX/UI', NOW()),
(8, 'Linux', 'soft_skill', 'Compétence système incontournable', NOW())
ON CONFLICT (id) DO NOTHING;

-- 4️⃣ Consultants
INSERT INTO consultants (id, user_id, company_id, title, bio, years_experience, hourly_rate, daily_rate, availability_date, status, created_at)
VALUES
(1, 3, 1, 'Développeur Frontend', 'Expert React et intégration UX.', 5, 65, 500, NOW(), 'AVAILABLE', NOW()),
(2, 4, 1, 'Data Scientist', 'Spécialiste en IA et traitement de données massives.', 3, 70, 550, NOW(), 'MISSION', NOW()),
(3, 5, 1, 'UX Designer', 'Designer spécialisée en expérience utilisateur.', 4, 60, 480, NOW(), 'AVAILABLE', NOW())
ON CONFLICT (id) DO NOTHING;

-- 5️⃣ Consultant Skills
INSERT INTO consultant_skills (consultant_id, skill_id)
VALUES
(1, 1),
(1, 6),
(2, 2),
(2, 3),
(3, 7)
ON CONFLICT DO NOTHING;

-- 6️⃣ Tenders
INSERT INTO tenders (id, title, description, company_id, status, created_at)
VALUES
(1, 'Mission Frontend React', 'Renfort d''équipe frontend pour projet e-commerce.', 1, 'OPEN', NOW()),
(2, 'Data Science - IA', 'Développement d''algorithmes de recommandation.', 1, 'IN_PROGRESS', NOW()),
(3, 'UX Designer', 'Optimisation de l''expérience utilisateur.', 1, 'OPEN', NOW())
ON CONFLICT (id) DO NOTHING;

-- 7️⃣ Tender Skills
INSERT INTO tender_skills (id, tender_id, skill_id)
VALUES
(1, 1, 1),
(2, 1, 6),
(3, 2, 2),
(4, 2, 3),
(5, 3, 7)
ON CONFLICT (id) DO NOTHING;