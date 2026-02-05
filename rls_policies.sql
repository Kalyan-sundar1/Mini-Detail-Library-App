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
