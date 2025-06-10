using System;
namespace prototype.Domain
{
	public class BaseResponse<T>
	{
		public string Description { get; set; }
		public int StatusCode { get; set; }
		public T Data { get; set; }
	}
}

