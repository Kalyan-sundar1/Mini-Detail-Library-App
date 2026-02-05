CREATE TABLE IF NOT EXISTS users (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    email text NOT NULL,
    role text CHECK (role IN ('admin','architect'))
);

ALTER TABLE details
ADD COLUMN IF NOT EXISTS source text,
ADD COLUMN IF NOT EXISTS user_id uuid REFERENCES users(id);

UPDATE details SET source='standard' WHERE id IN (1,2);
UPDATE details SET source='user_project' WHERE id=3;

UPDATE details
SET user_id='22222222-2222-2222-2222-222222222222'
WHERE id=3;

ALTER TABLE details ENABLE ROW LEVEL SECURITY;

CREATE POLICY admin_all_access
ON details
FOR SELECT
USING (
    current_setting('app.role', true) = 'admin'
);

CREATE POLICY architect_standard
ON details
FOR SELECT
USING (
    current_setting('app.role', true) = 'architect'
    AND source = 'standard'
);

CREATE POLICY architect_own
ON details
FOR SELECT
USING (
    current_setting('app.role', true) = 'architect'
    AND source='user_project'
    AND user_id::text = current_setting('app.user_id', true)
);

SELECT policyname, cmd, qual
FROM pg_policies
WHERE tablename='details';
