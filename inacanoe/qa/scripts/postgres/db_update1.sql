--

-- update InACanoe user
UPDATE public.user
    SET description = 'a person'
WHERE username = 'InACanoe' RETURNING *;