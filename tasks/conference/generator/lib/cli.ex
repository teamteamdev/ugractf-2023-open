defmodule Hellojoe.CLI do
  require Jason
  require Hellojoe

  def prefix, do: "ugra_meetings_need_to_be_emails_"
  def secret, do: "XPpwXF31ztr4FziNhFlQjPVjffvqlKyl"
  def suffix_size, do: 32

  def get_random_state(random_id) do
    <<a::size(56), b::size(56), _rest::binary>> = :crypto.hash(:md5, random_id)
    {:exsss, [a | b]}
  end

  def get_flag(random_id) do
    salt = :crypto.hash(:sha256, secret())
    hmac = :crypto.mac(:hmac, :sha256, salt, random_id)
    prefix() <> String.slice(Base.encode16(hmac, case: :lower), 0, suffix_size())
  end

  def split_flag(flag) do
    flag
      |> String.to_charlist
      |> Enum.chunk_every(3)
      |> Enum.map(&Base.encode16(List.to_string(&1), case: :lower))
  end

  def decode_flag(secrets) do
    secrets
      |> Enum.map(&Base.decode16!(&1, case: :lower))
      |> Enum.join
  end

  def main([random_id, workdir | _rest]) do
    attachments_path = Path.join(workdir, "attachments")

    Temp.track!
    {:ok, tmp_path} = Temp.path "conference"
    output_path = Path.join(tmp_path, "conference")
    File.mkdir_p(output_path)

    flag = get_flag(random_id)
    seed = get_random_state(random_id)
    actors = Hellojoe.names()
    secrets = split_flag(flag)

    :ok = Hellojoe.generate_modules(actors, secrets, output_path, seed)

    files =
      Path.wildcard(Path.join([output_path, "*"]))
      |> Enum.map(&String.to_charlist(Path.relative_to(&1, output_path)))
    out_zip = Path.join(attachments_path, "conference.zip") |> String.to_charlist
    :zip.create(out_zip, files, cwd: String.to_charlist(output_path))

    out = %{
      flags: [flag],
    }
    IO.puts(Jason.encode!(out))
  end
end
